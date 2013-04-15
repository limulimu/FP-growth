#coding=utf-8

# Copyright (C) Wei Li 
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# 
# This software is used for reseach only, which is for the project of Evmine.
# Evmine project contains viewer, explorer and deployer for EMR analytic.
# If you have any problem, contact me: lewe01@gmail.com.
# 
##
# @file fpgrowth.py
# @brief frequent itemset mining algorith of fp-growth
# @author Wei Li
# @version 1.0
# @date 2012-09-10

#The python file created by explorer which is part of Evmine project.
#Author: lewe
#Contact: Wei.Li@uts.edu.au
#Date: Tue Aug 21 2012 11:25:20 GMT+1000 (EST)


class DataMatrix(object):
    def __init__(self):
        self.matrix = {}

    def Show(self):
        for key in self.matrix.keys():
            print ' '.join(self.matrix[key])

    def GetData(self):
        return self.matrix
    def InitDataTest(self, size=100):
        #with open('./T10I4D100K.dat','r') as fp:
        with open('./test.dat','r') as fp:
            tid = 0
            ts = fp.readlines()
            for t in ts[:size]:
                self.matrix[tid] = t.split()
                tid = tid+1

        print "data size:",tid
    def InitDataCensus(self, size=100):
        with open('./census.dat','r') as fp:
        #with open('./test.dat','r') as fp:
            tid = 0
            ts = fp.readlines()
            for t in ts[:size]:
                its = t.split()
                self.matrix[tid] = [it.split('=')[1] for it in its[:-1]]
                tid = tid+1

        print "data size:",tid

##
# @brief fpgrowth tree
class FPTree(object):
    def __init__(self):
        self.root = FPNode(None)##root of the tree
        self.pathmap = {}## list for end nodes of the paths

    #def GetPathmap(self):
    #    return self.pathmap
    def __print_node__(self, node):
        if node:
            print '(',node.n_name,',',node.GetAttr('count'),')',
            if node.GetParent():
                print 'parent:',node.GetParent().n_name
            else:
                print ''
            if node.HasChild():
                for cnode in node.GetChildren():
                    self.__print_node__(cnode)


    def Show(self):
        self.__print_node__(self.root)

    ##
    # @brief add one record into the tree
    #
    # @param itemlist:one transaction record
    #
    # @return 
    def AddItemset(self, itemlist):#itemlist: 
        node = self.root
        #print 'add:',itemlist
        #flag = False ##create new node
        for item in itemlist:
            flag = False ##create new node
            childnode = node.GetChild(item)
            if not childnode: #create new node and insert into the tree
                childnode = FPNode(item)
                childnode.SetParent(node)
                childnode.SetAttr('count',1)
                node.AddChild(childnode)
                flag = True
            else: # increase the count of the node
                childnode.SetAttr('count',childnode.GetAttr('count')+1)
            node = childnode

            #print 'tree:',node.n_name
            if flag:
                if node.n_name in self.pathmap.keys():
                    self.pathmap[node.n_name].append(node)
                else:
                    self.pathmap[node.n_name] = [node]
        
        #print itemlist
        #print self.pathmap
    ##
    # @brief add one record into the tree
    #
    # @param itemlist:one transaction record
    #
    # @return 
    def AddItemsetWeight(self, itemlist):#itemlist: 
        #print itemlist, 'dddddddddddddd'
        node = self.root
        #print 'add:',itemlist
        #flag = False ##create new node
        for item in itemlist:
            flag = False ##create new node
            childnode = node.GetChild(item[0])
            if not childnode: #create new node and insert into the tree
                childnode = FPNode(item[0])
                childnode.SetParent(node)
                childnode.SetAttr('count',item[1])
                node.AddChild(childnode)
                flag = True
            else: # increase the count of the node
                childnode.SetAttr('count',childnode.GetAttr('count')+item[1])
            node = childnode

            #print 'tree:',node.n_name
            if flag:
                #print self.pathmap[node.n_name]
                #print 'ddddd',node.n_name
                if node.n_name in self.pathmap.keys():
                    self.pathmap[node.n_name].append(node)
                else:
                    self.pathmap[node.n_name] = [node]
        
        #print itemlist
        #print self.pathmap
        
    ##
    # @brief return all the path from item

    #
    # @param item: start bottom item in the tree
    #
    # @return 
    def TravelPathBottom(self, item): #  
        paths = []
        #print 'pathmap:',self.pathmap
        #print item,
        for node in self.pathmap[item]:
            path = []
            #node = node.GetParent()
            supc = node.GetAttr('count')  #add 2012-12-1
            while node.n_name:
                #path.append((node.n_name,node.GetAttr('count')))
                path.append((node.n_name,supc))  #modify 2012-12-1
                node = node.GetParent()
            paths.append(path)
            #print path

        return paths

##
# @brief fp tree node structure
class FPNode(object):
    def __init__(self, name):
        self.n_name = name
        self.n_attr = {}
        self.n_parent = None
        self.n_children = []

    def SetAttr(self, att_k, att_v):
        self.n_attr[att_k] = att_v

    def GetAttr(self, att_k):
        if att_k in self.n_attr.keys():
            return self.n_attr[att_k]
        else:
            return None

    def SetParent(self, pnode):
        self.n_parent = pnode

    def GetParent(self):
        return self.n_parent

    def AddChild(self, pnode):
        self.n_children.append(pnode)

    def AddChildren(self, pnodelist):
        self.n_children += pnodelist

    def delChild(self, pnode):
        self.n_children.remove(pnode)

    def GetChild(self, name):
        if not  self.HasChild():
            return None

        for child in self.n_children:
            if child.n_name == name:
                return child
        return None

    def HasChild(self):
        if self.n_children:
            return True
        else:
            return False

    def DelAttr(self, att_k):
        if att_k in self.n_attr.keys():
            del self.n_attr[att_k]

    def GetChildren(self):
        return self.n_children

    def GetParents(self):
        return self.n_parent


class Fpgrowth(object):
    def __init__(self):
        self.fis = {}
        self.items = {}
        self.atoms = []
        self.atommap = {}
        self.tree = FPTree()

    ##
    # @brief generate the frequent itemset : here not use the recursive
    #
    # @param enditem
    # @param paths
    #
    # @return 
    def Generate(self, enditem, paths):
        #print 'enditem.......:',enditem
        #print 'paths ........:',paths
        newtree = FPTree()
        candk = []
        candk.append(((enditem,),self.items[enditem]*1.0/self.size))
        #paths = filter(None, paths)
        #print 'ddddddd',paths
        if len(paths) > 0:            
            mergelist = {}
            for path in paths:
                for item in path[1:]:
                    if item[0] in mergelist.keys():
                        #mergelist[item[0]] += path[0][1]
                        mergelist[item[0]] += item[1]
                    else:
                        #mergelist[item[0]] = path[0][1]
                        mergelist[item[0]] = item[1]
            
            #print 'before',mergelist
            for key in mergelist.keys():
                if mergelist[key]/self.size < self.delt:
                #if mergelist[key] < self.items[enditem]:   #modifff
                    del mergelist[key]  
            #print 'after',mergelist        
            #new itemset with prefix enditem
            itemlist = mergelist.keys()
            #print itemlist,'eeeeeeeeeeeeee  '
            
            newpaths = []
            for path in paths:
                newpath = []
                for item in path[1:]:
                    if item[0] in itemlist:
                        newpath.append(item)
                newpaths.append(newpath)
            
            newpaths = filter(None, newpaths)            
                        
            #newitemset = self.Sortsub(mergelist.keys())
            #newdata = []
            #print 'newpaths:',newpaths
            for path in newpaths:
                newtree.AddItemsetWeight(path[:])
                
            ##
            newitemset = self.Sortsub(mergelist.keys())
            newitemset.reverse()
            for newitem in newitemset:
                #print 'current pattern base item:',item
                newpaths = newtree.TravelPathBottom(newitem)
                #print 'sssssssssssssss new',newitem
                #print 'sssssssssssssss old',enditem
                #print paths
                newpan = self.Generate(newitem, newpaths)
                #print enditem,'new pan:',newpan

                for pan in newpan:
                    candk.append(((enditem, ) + pan[0], min([self.items[enditem], pan[1], mergelist[newitem]*1.0/self.size])))
                    #print 'sssssssssssssss',(enditem, ) + pan[0],min([self.items[enditem], pan[1], mergelist[newitem]*1.0/self.size])
                    
                #print 'sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss'

        return candk

    ##
    # @brief sort the transaction data
    #
    # @param t
    #
    # @return 
    def Sortsub(self,t):
        sub = []
        for item in self.atoms:
            if item in t:
                sub.append(item)

        return sub

    ##
    # @brief main processing func.
    #
    # @param data
    # @param delt
    #
    # @return 
    def Processing(self, data, delt,delt1):
        #if the delt*size is one, then return.
        if delt*len(data) == 1:
            return
        #import time
        #print "Min sup:",delt
        self.delt = delt
        self.size = len(data)*1.0
        #start = time.clock()
        #sort the min sup. 1-itemset
        for key in data.keys():
            for d in data[key]:
                if d in self.items.keys():
                    self.items[d] += 1
                else:
                    self.items[d] = 1
        for it in self.items.keys():
            if self.items[it]/self.size < delt and self.items[it]/self.size > delt1:
            #if self.items[it]/self.size > delt:
                del self.items[it]
        self.atoms = [it[0] for it in sorted(self.items.items(), key=lambda x: x[1], reverse=True)]
        #print "sorted:",self.atoms
        #print 'First:',time.clock()-start
        #start = time.clock()

        #construct the fp tree
        for key in data.keys():
            t = self.Sortsub(data[key])
            #print t
            self.tree.AddItemset(t)

        #print  'Construct tree:',time.clock()-start
        #start = time.clock()
        #self.tree.Show()
        #find all the pattern from the fp tree
        self.atoms.reverse()
        #print "reversed sorted:",self.atoms
        for item in self.atoms:
            #print 'current pattern base item:',item
            paths = self.tree.TravelPathBottom(item)
            #print paths
            self.fis[item] = self.Generate(item, paths)
            #print '------------next item-----------------------\n'

        #print 'Find pattern:',time.clock()-start

    def GetPattern(self):
        return self.fis
    def Show(self):
        #print "*********************************************************"
        for key in self.fis.keys():
            #if len(self.fis[key]) <8:
            #    continue

            print "*********************************************************"
            #print "%s-items size:%d" % (key, len(self.fis[key]))
            print self.fis[key]
    
#dm = DataMatrix()
#dm.InitDataCensus(10000)
#dm.InitDataTest()
#dm.Show()

#ap = Fpgrowth()
#ap.Processing(dm.GetData(), 0.6)
#ap.Show()
