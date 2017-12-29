# -*- coding: utf-8 -*-
'''

@author: pgb
'''

from django.core.exceptions import ObjectDoesNotExist
import traceback
import sys
from TaskAndFlow.utility import *
from UserAndPrj.models import *
from TaskAndFlow.models import *
from TaskAndFlow.viewsimport import *
from TaskAndFlow.utility_filemanager import *

class ElFinderConnector():
    
    def __init__(self, volumes={}):
        self.httpResponse = {}
        self.httpStatusCode = 200
        self.httpHeader = {'Content-type': 'application/json'}
        self.data = {}
        self.response = {}
        self.return_view = None

        # Populate the volumes dict, using volume_id as the key
        self.volumes = {}
        for volume in volumes:
            self.volumes[volume.get_volume_id()] = volume

    def get_commands(self):
        """ Returns a dict which maps command names to functions.

            The dict key is the command name. The value is a tuple containing
            the name of a function on this class, and a dict specifying which
            GET variables must be set/unset. This lets us do validation of the
            given arguments, so the command functions can assume the correct
            values are set. Used by check_command_functions.
        """
        return {'open': ('__open', {'target': True}),
                'tree': ('__tree', {'target': True}),
                'file': ('__file', {'target': True}),
                'parents': ('__parents', {'target': True}),
                'mkdir': ('__mkdir', {'target': True, 'name': True}),
                'mkfile': ('__mkfile', {'target': True, 'name': True}),
                'rename': ('__rename', {'target': True, 'name': True}),
                'ls': ('__list', {'target': True}),
                'paste': ('__paste', {'targets[]': True, 'src': True,
                                      'dst': True, 'cut': True}),
                'rename': ('__rename', {'target': True, 'name': True}),
                'rm': ('__remove', {'targets[]': True}),
                'upload': ('__upload', {'target': True}),
                'search': ('__search', {'target': True}),
               }

    def get_init_params(self):
        """ Returns a dict which is used in response to a client init request.

            The returned dict will be merged with response during the __open
            command.
        """
        return {'api': '2.0',
                'uplMaxSize': '500M',
                'options': {'separator': '/',
                            'disabled': [],
                            'archivers': {'create': [],
                                          'extract': []},
                            'copyOverwrite': 1}
               }

    def get_allowed_http_params(self):
        """ Returns a list of parameters allowed during GET/POST requests.
        """
        return ['cmd', 'target', 'targets[]', 'current', 'tree',
                'name', 'content', 'src', 'dst', 'cut', 'init',
                'type', 'width', 'height', 'upload[]','q']

    def get_volume(self, hash):
        """ Returns the volume which contains the file/dir represented by the
            hash.
        """
        try:
            volume_id, target = hash.split('_')
        except ValueError:
            raise Exception('Invalid target hash: %s' % hash)

        return volume_id, target

    def check_command_variables(self, command_variables):
        """ Checks the GET variables to ensure they are valid for this command.
            _commands controls which commands must or must not be set.

            This means command functions do not need to check for the presence
            of GET vars manually - they can assume that required items exist.
        """
        for field in command_variables:
            if command_variables[field] == True and field not in self.data:
                return False
            elif command_variables[field] == False and field in self.data:
                return False
        return True

    def run_command(self, func_name, command_variables):
        """ Attempts to run the given command.

            If the command does not execute, or there are any problems
            validating the given GET vars, an error message is set.

            func: the name of the function to run (e.g. __open)
            command_variables: a list of 'name':True/False tuples specifying
            which GET variables must be present or empty for this command.
        """
        if not self.check_command_variables(command_variables):
            self.response['error'] = 'Invalid arguments'
            return

        func = getattr(self, '_' + self.__class__.__name__ + func_name, None)
        if not callable(func):
            self.response['error'] = 'Command failed'
            return

        try:
            func()
        except Exception, e:
            self.response['error'] = '%s' % e

    def run(self, request):
        """ Main entry point for running commands. Attemps to run a command
            function based on info in request.GET.

            The command function will complete in one of two ways. It can
            set response, which will be turned in to an HttpResponse and
            returned to the client.

            Or it can set return_view, a Django View function which will
            be rendered and returned to the client.
        """

        self.request = request

        # Is this a POST or a GET?
        if request.method == 'POST':
            data_source = request.POST
        elif request.method == 'GET':
            data_source = request.GET

        # Copy allowed parameters from the given request's GET to self.data
        for field in self.get_allowed_http_params():
            if field in data_source:
                if field == "targets[]":
                    self.data[field] = data_source.getlist(field)
                else:
                    self.data[field] = data_source[field]

        # If a valid command has been specified, try and run it. Otherwise set
        # the relevant error message.
        commands = self.get_commands()
        if 'cmd' in self.data:
            if self.data['cmd'] in commands:
                cmd = commands[self.data['cmd']]
                self.run_command(cmd[0], cmd[1])
            else:
                self.response['error'] = 'Unknown command'
        else:
            self.response['error'] = 'No command specified'

        self.httpResponse = self.response
        return self.httpStatusCode, self.httpHeader, self.httpResponse

    def __parents(self):
        """ Handles the parent command.

            Sets response['tree'], which contains a list of dicts representing
            the ancestors/siblings of the target object.

            The tree is not a tree in the traditional hierarchial sense, but
            rather a flat list of dicts which have hash and parent_hash (phash)
            values so the client can draw the tree.
        """
        target = self.data['target']
        volume_id,type = self.get_volume(target)
        if Directory.objects.filter(id=volume_id).count()>0:
            rootdir= Directory.objects.filter(id=volume_id)[0]
        else:
            rootdir= Directory.objects.filter(parent__isnull=True)[0]
        
        self.response['tree'] = []
       
        dirlist = Directory.objects.filter(parent=rootdir).order_by("index")
        for each in dirlist:
            self.response['tree'].append(self.getDirJsonByObj(each))
            
        filelist = Document.objects.filter(docdirectory=rootdir,version__isnull=True)
        for each in filelist:
            self.response['tree'].append(self.getFileJsonByObj(each, rootdir))

    def __tree(self):
        """ Handles the 'tree' command.

            Sets response['tree'] - a list of children of the specified
            target Directory.
        """
        target = self.data['target']
        #volume = self.get_volume(target)
        #self.response['tree'] = volume.get_tree(target)
        
        volume_id,type = self.get_volume(target)
        if Directory.objects.filter(id=volume_id).count()>0:
            rootdir= Directory.objects.filter(id=volume_id)[0]
        else:
            rootdir= Directory.objects.filter(parent__isnull=True)[0]
        
        self.response['tree'] = []
       
        dirlist = Directory.objects.filter(parent=rootdir).order_by("index")
        for each in dirlist:
            self.response['tree'].append(self.getDirJsonByObj(each))
            
        filelist = Document.objects.filter(docdirectory=rootdir,version__isnull=True)
        for each in filelist:
            self.response['tree'].append(self.getFileJsonByObj(each, rootdir))

    def __file(self):
        """ Handles the 'file' command.

            Sets return_view, which will cause read_file_view to be rendered
            as the response. A custom read_file_view can be given when
            initialising the connector.
        """
        target = self.data['target']
        volume = self.get_volume(target)

        # A file was requested, so set return_view to the read_file view.
        #self.return_view = self.read_file_view(self.request, volume, target)
        self.return_view = volume.read_file_view(self.request, target)

    def __open(self):
        """ Handles the 'open' command.

            Sets response['files'] and response['cwd'].

            If 'tree' is requested, 'files' contains information about all
            ancestors, siblings and children of the target. Otherwise, 'files'
            only contains info about the target's immediate children.

            'cwd' contains info about the currently selected directory.

            If 'target' is blank, information about the root dirs of all
            currently-opened volumes is returned. The root of the first
            volume is considered to be the current directory.
        """
        if 'tree' in self.data and self.data['tree'] == '1':
            inc_ancestors = True
            inc_siblings = True
        else:
            inc_ancestors = False
            inc_siblings = False

        target = self.data['target']
        if target == '':
            # No target was specified, which means the client is being opened
            # for the first time and requires information about all currently
            # opened volumes.

            # Assume the first volume's root is the currently open directory.
            rootdir= Directory.objects.filter(parent__isnull=True)[0]
        else:
            # A target was specified, so we only need to return info about
            # that directory.
            volume_id,type = self.get_volume(target)
            if Directory.objects.filter(id=volume_id).count()>0:
                rootdir= Directory.objects.filter(id=volume_id)[0]
            else:
                rootdir= Directory.objects.filter(parent__isnull=True)[0]
        


        #if 'tree' in self.data and self.data['tree'] == '1':
            #rootdir= Directory.objects.filter(parent__isnull=True)[0]

        dir=self.getDirJsonByObj(rootdir)

        self.response['cwd']=dir
        # Add relevant tree information for each volume
        #for volume_id in self.volumes:
        #    volume = self.volumes[volume_id]
        #    self.response['files'] = volume.get_tree('',
        #                                            inc_ancestors,
        #                                            inc_siblings)
        self.response['files']=[]
        #权限校验
       
        
        if 'tree' in self.data and self.data['tree'] == '1':
            treelist = []
            treedir = rootdir
            while treedir.parent:
                brodirlist = Directory.objects.filter(parent=treedir.parent).order_by("index")
                for each in brodirlist:
                    treelist.append(each)
                treedir = Directory.objects.get(id=treedir.parent.id)
            if  treedir != rootdir:
                self.response['files'].append(self.getDirJsonByObj(treedir))
            for index in range(len(treelist)):
                #print (treelist[len(treelist)-index-1])
                self.response['files'].append(self.getDirJsonByObj(treelist[len(treelist)-index-1]))
        
        if not rootdir.parent:
            self.response['files'].append(dir)
       
             
        dirlist = Directory.objects.filter(parent=rootdir).order_by("index")
        for each in dirlist:
            self.response['files'].append(self.getDirJsonByObj(each))
            
        filelist = Document.objects.filter(docdirectory=rootdir,version__isnull=True)
        for each in filelist:
            self.response['files'].append(self.getFileJsonByObj(each, rootdir))

        # If the request includes 'init', add some client initialisation
        # data to the response.
        if 'init' in self.data:
            self.response.update(self.get_init_params())

    def __mkdir(self):
        target = self.data['target']
        volume_id,type = self.get_volume(target)
        #self.response['added'] = [volume.mkdir(self.data['name'], target)]
        # if Directory.objects.filter(name=self.data['name']):
        #     raise Exception(u'存在重名文件夹！')
        each = Directory.objects.create(name=self.data['name'],parent_id=volume_id,creator=self.request.user)
        self.response['added'] =[]
        tmpdir={}
        tmpdir["isowner"] = 'false'
        tmpdir["ts"] = time.mktime(each.createtime.timetuple())
        tmpdir["mime"] = "directory"
        tmpdir["read"] = 1
        tmpdir["write"] = 1
        tmpdir["size"] = 0
        tmpdir["hash"] = '%d_%s' % (each.id, "dir")
        tmpdir["name"] = each.name
        tmpdir["phash"] = '%d_%s' % (int(volume_id), "dir")
        tmpdir["locked"] = 0
        tmpdir["dirs"] = 1
        self.response['added'].append(tmpdir)
    
    def getDirJsonByObj(self,each):
        auth = getDirAuth(each, self.request.user)
        tmpdir={}
        tmpdir["isowner"] = 'false'
        tmpdir["ts"] = time.mktime(each.createtime.timetuple())
        tmpdir["mime"] = "directory"
        tmpdir["read"] = 1 if auth>=4 else 0
        tmpdir["write"] = 1 if auth>=6 else 0
        tmpdir["size"] = 0
        tmpdir["hash"] = '%d_%s' % (each.id, "dir")
        tmpdir["name"] = each.name
        tmpdir["index"] = each.index if each.index else 0

        if each.parent:
            tmpdir["phash"] = '%d_%s' % (each.parent.id, "dir")
        if each.islock:
            tmpdir["locked"] = each.islock
        else:
            tmpdir["locked"] = 0 if self.request.user==each.creator else 1 
        tmpdir["dirs"] = 1
        tmpdir["remark"] = ''
      
        # dir["csscls"] = "elfinder-navbar-root-local"
        # dir["root"] = '%d_%s' % (rootdir.id, "dir")
        return tmpdir

    def getFileJsonByObj(self,each,parentdir):
        auth = getDirAuth(parentdir, self.request.user)
        tmpdir={}
        tmpdir["isowner"] = 'false'
        tmpdir["ts"] = time.mktime(each.createtime.timetuple())
        tmpdir["mime"] = each.filetype #todo 保存下来
        tmpdir["read"] = 1 if auth>=4 else 0
        tmpdir["write"] = 1 if auth>=6 else 0
        tmpdir["size"] = each.filesize
        tmpdir["hash"] = '%d_%s' % (each.id, "file")
        tmpdir["name"] = each.shortname
        tmpdir["phash"] = '%d_%s' % (parentdir.id, "dir")
        tmpdir["locked"] = 0 if auth>=6 else 1 
        tmpdir["url"] = '/%s%s' % (each.filepath, each.name)
        tmpdir["remark"] = each.remark if each.remark else ''
        
        return tmpdir
    
    def __mkfile(self):
        target = self.data['target']
        volume_id,type = self.get_volume(target)
        #self.response['added'] = [volume.mkfile(self.data['name'], target)]
        raise Exception(u'暂时不支持！')

    def __rename(self):
        target = self.data['target']
        #volume = self.get_volume(target)
        volume_id,type = self.get_volume(target)
        #self.response.update(volume.rename(self.data['name'], target))
        newname = self.data['name']
        self.response['removed'] = []
        self.response['added'] = []
        if type=='dir':
            if Directory.objects.filter(id=volume_id).count()==1:
                tar2rename = Directory.objects.get(id=volume_id)
                if Directory.objects.filter(name=newname).count()>0:
                    raise Exception(u'目录重名！')
                else:
                    tar2rename.name = newname 
                    tar2rename.save()
                    self.response['added'].append(self.getDirJsonByObj(tar2rename))
                    self.response['removed'].append(target)
            else:
                raise Exception(u'目录不存在！')
        elif type=='file':
            raise Exception(u'文件重命名不支持！')
        else:
            raise Exception(u'不支持的类型！')

    def __list(self):
        target = self.data['target']
        volume_id,type = self.get_volume(target)
        #self.response['list'] = volume.list(target)
        raise Exception(u'暂时不支持！')

    def __paste(self):
        targets = self.data['targets[]']
        source = self.data['src']
        dest = self.data['dst']
        cut = (self.data['cut'] == '1')
        source_volume,type = self.get_volume(source)
        dest_volume,type = self.get_volume(dest)
        if source_volume == dest_volume:
            raise Exception('源目录和目的目录相同！')
        
        if Directory.objects.filter(pk=int(source_volume)).count() == 1:
            sourcedir = Directory.objects.get(id=source_volume)
        else:
            raise Exception(u'源目录不存在！')
            
        if Directory.objects.filter(id=dest_volume).count() == 1:
            destdir = Directory.objects.get(id=dest_volume)
        else:
            raise Exception(u'目的目录不存在！')
        
        self.response['added'] = []
        self.response['removed'] = []
        
        #self.response.update(dest_volume.paste(targets, source, dest, cut))
        for target in targets:
            volume_id,type = self.get_volume(target)
            if type=='dir':
                if Directory.objects.filter(id=volume_id).count()==1:
                    tar= Directory.objects.get(id=volume_id)
                    if cut:
                        self.response['removed'].append('%d_%s' % (tar.id, "dir"))
                        tar.parent = destdir
                        tar.save()
                        self.response['added'].append(self.getDirJsonByObj(tar))
                        
                    else:
                        raise Exception(u'复制目录，暂时不支持！')
                else:
                    raise Exception(u'目录不存在！')
            elif type=='file':
                if Document.objects.filter(id=volume_id).count()==1:
                    tar = Document.objects.get(id=volume_id)
                    if cut:
                        tar.docdirectory.remove(sourcedir)
                        tar.docdirectory.add(destdir)
                        self.response['added'].append(self.getFileJsonByObj(tar,destdir))
                        #self.response['removed'].append(getFileJsonByObj(tar,sourcedir))
                    else:
                        tar.docdirectory.add(destdir)
                        self.response['added'].append(self.getFileJsonByObj(tar,destdir))
                else:
                    raise Exception(u'文件不存在！')
            else:
                raise Exception(u'不支持删除该类型！')

    def __remove(self):
        targets = self.data['targets[]']
        self.response['removed'] = []
        # Because the targets might not all belong to the same volume, we need
        # to lookup the volume and call the remove() function for every target.
        tar2dellist = []
        for target in targets:
            #volume = self.get_volume(target)
            #self.response['removed'].append(volume.remove(target))
            volume_id,type = self.get_volume(target)
            if type=='dir':
                if Directory.objects.filter(id=volume_id).count()==1:
                    tar2del = Directory.objects.get(id=volume_id)
                    if Document.objects.filter(docdirectory=tar2del).count()>0:
                        raise Exception(u'存在非空目录，不能删除！')
                    else:
                        tar2dellist.append(tar2del)
                else:
                    raise Exception(u'目录不存在！')
            elif type=='file':
                if Document.objects.filter(id=volume_id).count()==1:
                    tar2del = Document.objects.get(id=volume_id)
                    if Doc2Relate.objects.filter(document=tar2del).count()>0:
                        raise Exception(u'文件在使用，不能删除！')
                    else:
                        tar2dellist.append(tar2del)
                        createFileNotify(tar2del.docdirectory.all()[0].id,self.request.user,None, None, [tar2del])
                else:
                    raise Exception(u'文件不存在！')
            else:
                raise Exception(u'不支持删除该类型！')
        
        i=0        
        for target in targets:
            tar2dellist[i].delete()
            self.response['removed'].append(target)
            i = i + 1

            
    def __upload(self):
        parent = self.data['target']
        volume_id,type = self.get_volume(parent)
        files = self.request.FILES.getlist('upload[]')
        if Directory.objects.filter(id=volume_id).count()==1:
            filedir = Directory.objects.get(id=volume_id)
        else:
            raise Exception(u'目录不存在！')
        
        self.response['added'] = []
        self.response['removed'] = []
        for fileinfo in files:      
            name,filename=handle_uploaded_file(fileinfo)
            doc = Document()
            doc.name = filename
            doc.shortname = fileinfo.name
            doc.filepath = u"upload/"
            doc.creator=self.request.user
            doc.filesize = fileinfo._size
            doc.filetype = fileinfo.content_type
            doc.doctype='normal'
            doc.save()   
            
            doc.docdirectory.add(filedir)
            movefiletoDir(doc,filedir)
            
            self.response['added'].append(self.getFileJsonByObj(doc,filedir))
        #self.response.update(volume.upload(self.request.FILES, parent))
        
    def __search(self):
        """ Handles the 'tree' command.

            Sets response['tree'] - a list of children of the specified
            target Directory.
        """
        q = self.data['q']
        target = self.data['target']

        #volume = self.get_volume(target)
        #self.response['tree'] = volume.get_tree(target)
        if target!='all':
            volume_id,type = self.get_volume(target)
            if Directory.objects.filter(id=volume_id).count()>0:
                rootdir= Directory.objects.filter(id=volume_id)[0]
            else:
                rootdir= Directory.objects.filter(parent__isnull=True)[0]
            
            self.response['files'] = []
           
            dirlist = Directory.objects.filter(Q(parent=rootdir)&Q(name__contains =q))
            for each in dirlist:
                self.response['files'].append(self.getDirJsonByObj(each))
                
            filelist = Document.objects.filter(Q(docdirectory=rootdir)&Q(shortname__contains =q)&Q(version__isnull=True))
            for each in filelist:
                self.response['files'].append(self.getFileJsonByObj(each, rootdir))
        else:
            self.response['files'] = []
            rootdir= Directory.objects.filter(parent__isnull=True)[0]
            dirlist = Directory.objects.filter(Q(name__contains =q))
            for each in dirlist:
                self.response['files'].append(self.getDirJsonByObj(each))
                
            filelist = Document.objects.filter(Q(shortname__contains =q)&Q(version__isnull=True))
            for each in filelist:
                self.response['files'].append(self.getFileJsonByObj(each, each.docdirectory.all()[0] if each.docdirectory.all() else rootdir))
