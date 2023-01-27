#include <iostream>

using namespace std;
template <typename keytype, typename valuetype>
class Node{
public:
    Node* leftChild;
    Node* rightChild;
    Node* parent;
    valuetype value;
    keytype key;
    bool isRed;
    int subSize;

    Node<keytype,valuetype>(){
        leftChild = NULL;
        rightChild = NULL;
        parent = NULL;
        subSize = 0;
    }

    Node(keytype newKey, valuetype newValue){
        leftChild = NULL;
        rightChild = NULL;
        parent = NULL;
        value = newValue;
        key = newKey;
        subSize = 0;
    }
};

template <typename keytype, typename valuetype>
class RBTree{
private:
    Node<keytype,valuetype>* head;                           
    int sizeTree;
    Node<keytype,valuetype>* nil;                                                                                                                                                                                          ;
public:

    RBTree<keytype,valuetype>(const RBTree<keytype,valuetype>& src){
        deepCopy(src);
    }

    void deepCopy(const RBTree<keytype,valuetype>& src){ //Copy nil dummy node/head, then preorder traversal down to copy
        sizeTree = src.sizeTree;
        nil = new Node<keytype,valuetype>();
        nil->isRed = false;
        nil->leftChild = nil;
        nil->rightChild = nil;
        nil->parent = nil;
        head = new Node<keytype,valuetype>(src.head->key, src.head->value);
        head->isRed = false;
        head->parent = nil;
        if (src.head->leftChild != src.nil){
            head->leftChild = copier(src.head->leftChild, src.nil);
            head->leftChild->parent = head;
        }
        if(src.head->rightChild != src.nil){
            head->rightChild = copier(src.head->rightChild, src.nil);
            head->rightChild->parent = head;
        }
    }

    Node<keytype,valuetype>* copier(Node<keytype,valuetype>* head, Node<keytype,valuetype>* useNil){ //Helper to copy in traversal
        Node<keytype,valuetype>* temp = new Node<keytype,valuetype>(head->key,head->value);

        temp->isRed = head->isRed;

        if (head->leftChild == useNil){
            temp->leftChild = nil;
        }
        if (head->rightChild == useNil){
            temp->rightChild = nil;
        }
        if (head->leftChild != useNil){
            temp->leftChild = copier(head->leftChild, useNil);
            temp->leftChild->parent = temp;
        }
        if (head->rightChild != useNil){
            temp->rightChild = copier(head->rightChild, useNil);
            temp->rightChild->parent = temp;
        }

        return temp;
    }

    const RBTree<keytype,valuetype> & operator=(const RBTree<keytype,valuetype> &src){
        if (this != &src){
            DestructorFunction(head);
            delete nil;
            deepCopy(src);
        }
        return *this;
    }

    RBTree<keytype,valuetype>(){//Default const, nil dummy node only
        nil = new Node<keytype,valuetype>();
        nil->isRed = false;
        nil->leftChild = nil;
        nil->rightChild = nil;
        nil->parent = nil;
        nil->subSize = 0;
        head = nil;
        sizeTree = 0;
    }

    RBTree<keytype,valuetype>(keytype k[],valuetype v[],int s){ //Repeated Insert constructor
        nil = new Node<keytype,valuetype>();
        nil->isRed = false;
        nil->leftChild = nil;
        nil->rightChild = nil;
        nil->parent = nil;
        head = nil;
        nil->subSize = 0;
        sizeTree = 0;
        for (int i = 0; i < s; i++){
            insert(k[i],v[i]);
        }
    }

    ~RBTree<keytype,valuetype>(){ //Postorder traversal for deletion, starting at head, delete nil dummy at the end
        DestructorFunction(head);
        delete nil;
    }

    void DestructorFunction(Node<keytype,valuetype>* node){
        if (node != nil){
            DestructorFunction(node->leftChild);
            DestructorFunction(node->rightChild);
            delete node;
        }

    }
    
    valuetype* search(keytype k){ 
        return searchHelper(head, k);
    }

    valuetype* searchHelper(Node<keytype,valuetype>* temp, keytype k){ //Traditional binary search
        if (temp == nil){
            return NULL;
        }

        if (temp->key == k){
            return &temp->value;
        }

        if (temp->key < k){
            return searchHelper(temp->rightChild, k);
        }

        return searchHelper(temp->leftChild, k);
    }

    Node<keytype,valuetype>* returnNodeRef(Node<keytype,valuetype>* temp ,keytype k){ //Traversal to find needed node
        if (temp == nil){
            return nil;
        }

        if (temp->key == k){
            return temp;
        }

        if (temp->key < k){
            return returnNodeRef(temp->rightChild,k);
        }

        return returnNodeRef(temp->leftChild, k);
    }

    Node<keytype,valuetype>* returnNodeRefADJUST(Node<keytype,valuetype>* temp, keytype k){ //Traversal to find needed node to delete, decreases sub tree lengths premptively
        if (temp == nil){
            return nil;
        }

        if (temp->key == k){
            return temp;
        }

        if (temp->key < k){
            temp->subSize--;
            return returnNodeRefADJUST(temp->rightChild,k);
        }
        temp->subSize--;
        return returnNodeRefADJUST(temp->leftChild, k);
    }

    Node<keytype,valuetype>* returnNodeReADJUST(Node<keytype,valuetype>* temp, keytype k){ //Readjusts subtree lengths if node to delete is never found
        if (temp == nil){
            return nil;
        }

        if (temp->key == k){
            return temp;
        }

        if (temp->key < k){
            temp->subSize++;
            return returnNodeReADJUST(temp->rightChild,k);
        }
        temp->subSize++;
        return returnNodeReADJUST(temp->leftChild, k);
    }

    void insertfixer(Node<keytype,valuetype>* z){ //Fix RB Violation
        Node<keytype,valuetype>* y = nil; 
        while (z->parent->isRed == true){ //While Double Red Violation
            if (z->parent == z->parent->parent->leftChild){ //If parent is a left child
                y = z->parent->parent->rightChild; 
                if (y->isRed){
                    z->parent->isRed = false;
                    y->isRed = false;
                    z->parent->parent->isRed = true;
                    z = z->parent->parent;
                }
                else{
                    if (z == z->parent->rightChild){
                        z = z->parent;
                        leftRotate(z);
                    }

                    z->parent->isRed = false;
                    z->parent->parent->isRed = true;
                    rightRotate(z->parent->parent);
                }
               
            }
            else{
                y = z->parent->parent->leftChild;
                if (y->isRed){
                    z->parent->isRed = false;
                    y->isRed = false;
                    z->parent->parent->isRed = true;
                    z = z->parent->parent;
                }
                else{
                    if (z == z->parent->leftChild){
                        z = z->parent;
                        rightRotate(z);
                    }

                    z->parent->isRed = false;
                    z->parent->parent->isRed = true;
                    leftRotate(z->parent->parent);
                }

            }
        }
        head->isRed = false;
    }
    void insert(keytype k, valuetype v){ //Place into correct place in tree, disregarding RB rules
        Node<keytype,valuetype>* temp = new Node<keytype,valuetype>(k,v);
        temp->leftChild = nil;
        temp->rightChild = nil;
        temp->parent = nil;

        Node<keytype,valuetype>* y = nil; //Future parent of new node
        Node<keytype,valuetype>* x = head;

        while (x != nil){
            y = x; 
            if (temp->key < x->key){
                x->subSize++;
                x = x->leftChild;
            }
            else{
                x->subSize++;
                x = x->rightChild;
            }
        }
        temp->parent = y;
        if (y == nil){
            head = temp;
        }
        else if (temp->key < y->key){
            y->leftChild = temp;
        }
        else{
            y->rightChild = temp;
        }
        temp->leftChild = nil;
        temp->rightChild = nil;
        temp->isRed = true;
        temp->subSize = 1;
        insertfixer(temp);
        sizeTree++;
    }

    int remove(keytype k){
        Node<keytype,valuetype>* z = returnNodeRefADJUST(head,k); //Node to be removed
        if (z == nil){
            z = returnNodeReADJUST(head,k);
            return 0;
        }
         
        Node<keytype,valuetype>* y; 
        Node<keytype,valuetype>* x;

        y = z;
        bool originalcolor = y->isRed;
        if (z->leftChild == nil){
            x =  z->rightChild;
            transplant(z, z->rightChild);
            delete z;
        }

        else if (z->rightChild == nil){
            x = z->leftChild;
            transplant(z,z->leftChild);
            delete z;
        }

        else{ //Replace by pred.
            y = treeMaximumADJUST(z->leftChild); //Pred
            originalcolor = y->isRed;
            x = y->leftChild;
            if (y->parent == z){
                x->parent = y;
            }
            else{
                transplant(y,y->leftChild);
                y->leftChild = z->leftChild;
                y->leftChild->parent = y;
            }
            transplant(z,y);
            y->rightChild = z->rightChild;
            y->rightChild->parent = y;
            y->isRed = z->isRed;
            
            if (originalcolor == false){
                removeFixer(x);
            }
            delete z;
        }
        sizeTree--;
        return 1;
    }

    keytype select(int pos){
        return selectFind(head,pos);
    }

    keytype selectFind(Node<keytype,valuetype>* x, int i){
        int r = x->leftChild->subSize + 1;
        
        if (i == r){
            return x->key;
        }

        else if(i < r){
            return selectFind(x->leftChild, i);
        }
        else{
            return selectFind(x->rightChild, i - r);
        }
    }

    int rank(keytype k){
        Node<keytype,valuetype>* temp = returnNodeRef(head,k);

        return rankCalc(temp);
    }

    int rankCalc(Node<keytype,valuetype>* x){
        int r = x->leftChild->subSize + 1;
        Node<keytype,valuetype>* y;

        y = x;
        
        while (y != head){
            if (y == y->parent->rightChild){
                r = r + y->parent->leftChild->subSize + 1;
            }
            y = y->parent;
        }
        return r;
    }

    void removeFixer(Node<keytype,valuetype>* x){ //One of removed children
        Node<keytype,valuetype>* w;
        while (x != head && x->isRed == false){ //While node is still black, need red to restore RB Rules
            if (x == x->parent->leftChild){ //If 
                w = x->parent->rightChild;
                if (w->isRed){
                    w->isRed = false;
                    x->parent->isRed = true;
                    leftRotate(x->parent);
                    w = x->parent->rightChild;
                }
                if (w->leftChild->isRed == false && w->rightChild->isRed == false){
                    w->isRed = true;
                    x = x->parent;
                }

                else{
                    if (w->rightChild->isRed == false){
                        w->leftChild->isRed == false;
                        w->isRed == true;
                        rightRotate(w);
                        w = x->parent->rightChild;
                    }
                    w->isRed = x->parent->isRed;
                    x->parent->isRed = false;
                    w->rightChild->isRed = false;
                    leftRotate(x->parent);
                    x = head;
                }
            }
            else{
                w = x->parent->leftChild;
                if (w->isRed){
                    w->isRed = false;
                    x->parent->isRed = true;
                    rightRotate(x->parent);
                    w = x->parent->leftChild;
                }
                if (w->rightChild->isRed == false && w->leftChild->isRed == false){
                    w->isRed = true;
                    x = x->parent;
                }

                else{
                    if (w->leftChild->isRed == false){
                        w->rightChild->isRed == false;
                        w->isRed == true;
                        leftRotate(w);
                        w = x->parent->leftChild;
                    }
                    w->isRed = x->parent->isRed;
                    x->parent->isRed = false;
                    w->leftChild->isRed = false;
                    rightRotate(x->parent);
                    x = head;
                }
            }
        }
        x->isRed = false;
    }
    void transplant(Node<keytype,valuetype>* u, Node<keytype,valuetype>* v){ //Helper to replace subtree of one tree, with another
        if (u->parent == nil){
            head = v;
        }
        else if (u == u->parent->leftChild){
            u->parent->leftChild = v;
        }
        else{
            u->parent->rightChild = v;
        }
        v->parent = u->parent;
    }

    Node<keytype,valuetype>* treeMinimum(Node<keytype,valuetype>* x){ //returns min, given head, of subtree
        while (x->leftChild != nil){
            x = x->leftChild;
        }
        return x;
    }

    Node<keytype,valuetype>* treeMaximum(Node<keytype,valuetype>* x){ //return max, given head, of subtree
        while (x->rightChild != nil){
            x = x->rightChild;
        }
        return x;
    }

    Node<keytype,valuetype>* treeMaximumADJUST(Node<keytype,valuetype>* x){ //Returns max of given subtree, decrementing premptively for delete
        while (x->rightChild != nil){
            x->subSize--;
            x = x->rightChild;
        }
        return x;
    }
    
    keytype* successor(keytype k){ //returns successor of given key
        Node<keytype,valuetype>* x = returnNodeRef(head,k);

        if (x == nil){
            return NULL;
        }

        if (x->rightChild != nil){
            Node<keytype,valuetype>* ans = treeMinimum(x->rightChild);
            return &ans->key;
        }

        Node<keytype,valuetype>* y = x->parent;
        while (y != nil && x == y->rightChild){
            x = y;
            y = y->parent;
        }

        if(y == nil){
            return NULL;
        }

        return &y->key;
    }
    
    keytype* predecessor(keytype k){ //Returns predecessor of given key
        Node<keytype,valuetype>* x = returnNodeRef(head,k);

        if (x == nil){
            return NULL;
        }

        if (x->leftChild != nil){
            Node<keytype,valuetype>* ans = treeMaximum(x->leftChild);
            return &ans->key;
        }
        Node<keytype,valuetype>* y = x->parent;
        while (y != nil && x == y->leftChild){
            x = y;
            y = y->parent;
        }

        if (y == nil){
            return NULL;
        }

        return &y->key;
    }

    int size(){
        return sizeTree;
    }

    void preorder(){
        preorderHelper(head);
        cout << endl;
    }

    void inorder(){
        inorderHelper(head);
        cout << endl;
    }

    void postorder(){
        postorderHelper(head);
        cout << endl;
    }

    void preorderHelper(Node<keytype,valuetype>* temp){
        if (temp == nil){
            return;
        }

        cout << temp->key << " ";
        preorderHelper(temp->leftChild);
        preorderHelper(temp->rightChild);
    }

    void inorderHelper(Node<keytype,valuetype>* temp){
        if (temp == nil){
            return;
        }
        inorderHelper(temp->leftChild);
        cout << temp->key << " ";
        inorderHelper(temp->rightChild);
    }

    void postorderHelper(Node<keytype,valuetype>* temp){
        if (temp == nil){
            return;
        }

        postorderHelper(temp->leftChild);
        postorderHelper(temp->rightChild);
        cout << temp->key << " ";
    }
    void printk(int k){
        int counter = 0;
        int dummy = printHelper(k,counter, head);
        cout << endl;
    }

    int printHelper(int k, int counter, Node<keytype,valuetype>* temp){ //Prints k nodes, in tree, passes counter up to keep track of how many have been printed out
        if (temp == nil || counter >= k){
            return 0;
        }
        else{
            counter = counter + printHelper(k, counter,temp->leftChild);

            if (counter < k){
                cout << temp->key << " ";
                counter+= 1;
            }
            counter = counter + printHelper(k, counter,temp->rightChild);
            return counter;
        }
    }

    void leftRotate(Node<keytype,valuetype>* x){
        Node<keytype,valuetype>* y;
        y = x->rightChild;
        x->rightChild = y->leftChild;
        if (y->leftChild != nil){
            y->leftChild->parent = x;
        }
        y->parent = x->parent;
        if (x->parent == nil){
            head = y;
        }
        else if (x == x->parent->leftChild){
            x->parent->leftChild = y;
        }
        else{
            x->parent->rightChild = y;
        }
        y->leftChild = x;
        x->parent = y;
        y->subSize = x->subSize;
        x->subSize = x->leftChild->subSize + x->rightChild->subSize + 1;
    }
    void rightRotate(Node<keytype,valuetype>* x){
        Node<keytype,valuetype>* y;
        y = x->leftChild;
        x->leftChild = y->rightChild;
        if (y->rightChild != nil){
            y->rightChild->parent = x;
        }
        y->parent = x->parent;
        if (x->parent == nil){
            head = y;
        }
        else if (x == x->parent->rightChild){
            x->parent->rightChild = y;
        }
        else{
            x->parent->leftChild = y;
        }
        y->rightChild = x;
        x->parent = y;
        y->subSize = x->subSize;
        x->subSize = x->leftChild->subSize + x->rightChild->subSize + 1;
    }
};