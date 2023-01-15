from random import shuffle

class BinaryTreeNode:
    def __init__(self,value,parent,left_child,right_child):
        self.value = value
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child
    
    def get_value(self):
        return self.value
    
    def get_parent(self):
        return self.parent
    
    def get_left_child(self):
        return self.left_child
    
    def get_right_child(self):
        return self.right_child
    
    def set_value(self,value):
        self.value = value
    
    def set_parent(self,parent):
        self.parent = parent
    
    def set_left_child(self,left_child):
        self.left_child = left_child
    
    def set_right_child(self,right_child):
        self.right_child = right_child
    
    def reset(self):
        self.value = None
        self.parent = None
        self.left_child = None
        self.right_child = None

class BinaryTree:
    def __init__(self,original_array): # original_arrayは数値が格納されたシーケンス
        original_array=list(original_array)
        self.root=0
        self.garbage=set()
        if not original_array:
            self.tree_array=[]
            self.length=0
            self.array_length=0
            return
        shuffle(original_array)
        self.tree_array=[BinaryTreeNode(original_array[0],None,None,None)]
        self.length=1 # 見かけの長さ（木のノード数）
        self.array_length=1 # tree_arrayの実際の長さ
        for i in range(1,len(original_array)):
            new_value=original_array[i]
            index=self.root
            while True:
                compared_node=self.get_node(index)
                compared_value=compared_node.get_value()
                if new_value<compared_value:
                    new_index=compared_node.get_left_child()
                    if new_index!=None:
                        index=new_index
                    else:
                        compared_node.set_left_child(self.length)
                        self.tree_array.append(BinaryTreeNode(new_value,index,None,None))
                        self.length+=1
                        self.array_length+=1
                        break
                elif new_value==compared_value:
                    break
                else:
                    new_index=compared_node.get_right_child()
                    if new_index!=None:
                        index=new_index
                    else:
                        compared_node.set_right_child(self.length)
                        self.tree_array.append(BinaryTreeNode(new_value,index,None,None))
                        self.length+=1
                        self.array_length+=1
                        break
    
    def get_node(self, index):
        return self.tree_array[index]

    def search(self,target): # 検索機能。targetが存在する場合はtargetのインデックスを返し、存在しない場合は-1を返す
        index=self.root
        while True:
            compared_node=self.get_node(index)
            compared_value=compared_node.get_value()
            if target<compared_value:
                new_index=compared_node.get_left_child()
                if new_index!=None:
                    index=new_index
                else:
                    return -1
            elif target==compared_value:
                return index
            else:
                new_index=compared_node.get_right_child()
                if new_index!=None:
                    index=new_index
                else:
                    return -1
    
    def show_contents(self): # tree_arrayの中身を表示
        for node in self.tree_array:
            print(node.get_value(),node.get_parent(),node.get_left_child(),node.get_right_child())
    
    def add(self,value): # valueを追加したうえでTrueを返す。すでにvalueが存在する場合はFalseを返す

        def find_space(value,index):
            used_space=None
            if self.garbage:
                used_space = self.garbage.pop()
                used_node=self.get_node(used_space)
                used_node.set_value(value)
                used_node.set_parent(index)
            else:
                used_space = self.array_length
                self.array_length+=1
                self.tree_array.append(BinaryTreeNode(value,index,None,None))
            self.length+=1
            return used_space
        
        if self.length <= 0:
            self.root = find_space(value,None)
            return True
        index=self.root
        while True:
            compared_node=self.get_node(index)
            compared_value=compared_node.get_value()
            if value<compared_value:
                new_index=compared_node.get_left_child()
                if new_index!=None:
                    index=new_index
                else:
                    compared_node.set_left_child(find_space(value,index))
                    return True
            elif value==compared_value:
                return False
            else:
                new_index=compared_node.get_right_child()
                if new_index!=None:
                    index=new_index
                else:
                    compared_node.set_right_child(find_space(value,index))
                    return True
    
    def smallest(self): # 最小値を返す
        node=self.get_node(self.root)
        left_child=node.get_left_child()
        while left_child!=None:
            node=self.get_node(left_child)
            left_child=node.get_left_child()
        return node.get_value()
    
    def largest(self): # 最大値を返す
        node=self.get_node(self.root)
        right_child=node.get_right_child()
        while right_child!=None:
            node=self.get_node(right_child)
            right_child=node.get_right_child()
        return node.get_value()
    
    def smaller_sort(self, length): # 小さい方からlength番目までソートしてリストで返す
        index=self.root
        result=[]
        visited=set()
        cnt=0
        while cnt<length:
            node=self.get_node(index)
            left_child=node.get_left_child()
            if left_child!=None and left_child not in visited:
                index=left_child
            else:
                if index not in visited:
                    result.append(node.get_value())
                    visited.add(index)
                    cnt+=1
                right_child=node.get_right_child()
                if right_child!=None and right_child not in visited:
                    index=right_child
                else:
                    parent=node.get_parent()
                    if parent!=None:
                        index=parent
                    else:
                        break
        return result
    
    def smaller_sort_all(self): # 木全体を昇順ソートしてリストで返す
        return self.smaller_sort(self.length)
    
    def larger_sort(self, length): # 大きい方からlength番目までソートしてリストで返す
        index=self.root
        result=[]
        visited=set()
        cnt=0
        while cnt<length:
            node=self.get_node(index)
            right_child=node.get_right_child()
            if right_child!=None and right_child not in visited:
                index=right_child
            else:
                if index not in visited:
                    result.append(node.get_value())
                    visited.add(index)
                    cnt+=1
                left_child=node.get_left_child()
                if left_child!=None and left_child not in visited:
                    index=left_child
                else:
                    parent=node.get_parent()
                    if parent!=None:
                        index=parent
                    else:
                        break
        return result
    
    def larger_sort_all(self): # 木全体を降順ソートしてリストで返す
        return self.larger_sort(self.length)
    
    def delete(self, value): # 要素を削除する。削除出来たらTrueを返し、指定した要素が存在しなかったらFalseを返す
        if self.length <= 0:
            return False
        deleted=self.search(value) # 削除対象ノードのインデックス
        if deleted < 0:
            return False
        deleted_node=self.get_node(deleted) #削除対象ノード
        parent=deleted_node.get_parent() # 削除対象の親ノードのインデックス。Noneを考慮する必要あり
        target_left=deleted_node.get_left_child()
        target_right=deleted_node.get_right_child()
        if target_left != None:
            target_left_node=self.get_node(target_left)
            index=target_left
            node=self.get_node(index)
            right_child=node.get_right_child()
            while right_child!=None:
                index=right_child
                node=self.get_node(index)
                right_child=node.get_right_child() # indexは削除対象ノードと入れ替わるノードのインデックス
            if parent != None:
                parent_node=self.get_node(parent)
                if parent_node.get_value() - deleted_node.get_value() > 0:
                    parent_node.set_left_child(index) # 親の左子書き換え
                else:
                    parent_node.set_right_child(index) # 親の右子書き換え
            else:
                self.root=index
            if target_right != None:
                node.set_right_child(target_right) # 代替ノードの右子書き換え
                target_right_node=self.get_node(target_right)
                target_right_node.set_parent(index) # target_rightの親書き換え
            if index != target_left:
                target_left_node.set_parent(index) # target_leftの親書き換え
                index_parent=node.get_parent()
                index_parent_node=self.get_node(index_parent)
                index_left=node.get_left_child()
                node.set_left_child(target_left) # 代替ノードの左子書き換え
                index_parent_node.set_right_child(index_left) # index_parentの右子書き換え
                if index_left != None:
                    index_left_node=self.get_node(index_left)
                    index_left_node.set_parent(index_parent) # index_leftの親書き換え
            node.set_parent(deleted_node.get_parent()) # 代替ノードの親書き換え
            deleted_node.reset()
            self.garbage.add(deleted)
            self.length-=1
            return True
        elif target_right != None: # 削除対象ノードが右子のみ持つ場合
            target_right_node = self.get_node(target_right)
            index=target_right
            node=self.get_node(index)
            left_child=node.get_left_child()
            while left_child!=None:
                index=left_child
                node=self.get_node(index)
                left_child=node.get_left_child() # indexは削除対象ノードと入れ替わるノードのインデックス
            if parent != None:
                parent_node=self.get_node(parent)
                if parent_node.get_value() - deleted_node.get_value() > 0:
                    parent_node.set_left_child(index) # 親の左子書き換え
                else:
                    parent_node.set_right_child(index) # 親の右子書き換え
            else:
                self.root=index
            if index != target_right:
                target_right_node.set_parent(index) # target_rightの親書き換え
                index_parent=node.get_parent()
                index_parent_node=self.get_node(index_parent)
                index_right=node.get_right_child()
                node.set_right_child(target_right) # 代替ノードの右子書き換え
                index_parent_node.set_left_child(index_right) # index_parentの左子書き換え
                if index_right != None:
                    index_right_node=self.get_node(index_right)
                    index_right_node.set_parent(index_parent) # index_rightの親書き換え
            node.set_parent(deleted_node.get_parent()) # 代替ノードの親書き換え
            deleted_node.reset()
            self.garbage.add(deleted)
            self.length-=1
            return True
        else: # 削除対象ノードが子を持たない場合
            if parent != None:
                parent_node=self.get_node(parent)
                if parent_node.get_value() - deleted_node.get_value() > 0:
                    parent_node.set_left_child(None) # 親の左子書き換え
                else:
                    parent_node.set_right_child(None) # 親の右子書き換え
            deleted_node.reset()
            self.garbage.add(deleted)
            self.length-=1
            return True