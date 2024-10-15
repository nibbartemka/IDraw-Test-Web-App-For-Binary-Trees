class BinarySearchTree extends TreeBase {
    constructor() {
        super();
    };

    insert(data, hasDublicate=false, isDublicateLeft=false) {
        let newNode = new NodeBST(data);
        if (this.root === null) {
            this.root = newNode;
        } else {
            this.insertNode(this.root, newNode, hasDublicate, isDublicateLeft);
        };
    };

    insertNode(node, newNode, hasDublicate=false, isDublicateLeft=false) {
        if (hasDublicate) {
            if (isDublicateLeft) {
                if (newNode.data <= node.data){
                    if (node.left === null) {
                        node.left = newNode;
                    } else {
                        this.insertNode(node.left, newNode, hasDublicate, isDublicateLeft);
                    };
                } else if (newNode.data > node.data) {
                    if (node.right === null) {
                        node.right = newNode;
                    } else {
                        this.insertNode(node.right, newNode, hasDublicate, isDublicateLeft);
                    };
                };
            } else {
                if (newNode.data < node.data){
                    if (node.left === null) {
                        node.left = newNode;
                    } else {
                        this.insertNode(node.left, newNode, hasDublicate, isDublicateLeft);
                    };
                } else if (newNode.data >= node.data) {
                    if (node.right === null) {
                        node.right = newNode;
                    } else {
                        this.insertNode(node.right, newNode, hasDublicate, isDublicateLeft);
                    };
                };
            }

        } else {
            if (newNode.data < node.data){
                if (node.left === null) {
                    node.left = newNode;
                } else {
                    this.insertNode(node.left, newNode, hasDublicate, isDublicateLeft);
                };
            } else if (newNode.data > node.data) {
                if (node.right === null) {
                    node.right = newNode;
                } else {
                    this.insertNode(node.right, newNode, hasDublicate, isDublicateLeft);
                };
            };
        }
    }

    remove(data, isMaxLeft=false) {
        this.root = this.removeNode(this.root, data, isMaxLeft);
    }

    removeNode(node, data, isMaxLeft=false) {
        if (node === null) {
            return null;
      
        } else if (data < node.data) {
            node.left = this.removeNode(node.left, data, isMaxLeft);
            return node;

        } else if (data > node.data) {
            node.right = this.removeNode(node.right, data, isMaxLeft);
            return node;
      
        } else {
           
            if (node.left === null && node.right === null) {
                node = null;
                return node;
            }

            if (node.left === null) {
                node = node.right;
                return node;
            } else if(node.right === null) {
                node = node.left;
                return node;
            }
            
            let newNode;
            if (isMaxLeft) {
                newNode = this.maxNode(node.left);
                node.data = newNode.data;
                node.left = this.removeNode(node.left, newNode.data, isMaxLeft);
            } else {
                newNode = this.minNode(node.right);
                node.data = newNode.data;
                node.right = this.removeNode(node.right, newNode.data, isMaxLeft);
            }
            
            return node;
        }
    }
}