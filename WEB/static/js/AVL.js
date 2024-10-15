const MAX_RIGHT_OVERWEIGHT = 1
const MAX_LEFT_OVERWEIGHT = -1

class AVLTree extends TreeBase {
  constructor() {
      super();
  }


  getNodeHeight(node) {
    if (node === null){
      return 0;
    };
    return node.height;
  }

  rightRotate(y) {
    let x = y.left;
    let T2 = x.right;

    x.right = y;
    y.left = T2;

    y.height = Math.max(this.getNodeHeight(y.left), this.getNodeHeight(y.right)) + 1;
    x.height = Math.max(this.getNodeHeight(x.left), this.getNodeHeight(x.right)) + 1;
    
    return x;
  }

  leftRotate(x) {
    let y = x.right;
    let T2 = y.left;
    
    y.left = x;
    x.right = T2;
    
    x.height = Math.max(this.getNodeHeight(x.left), this.getNodeHeight(x.right)) + 1;
    y.height = Math.max(this.getNodeHeight(y.left), this.getNodeHeight(y.right)) + 1;
    
    return y;
  }

  getBalanceFactor(node) {
    if (node == null){
      return 0;
    }
    
    return this.getNodeHeight(node.left) - this.getNodeHeight(node.right);
  }


  insertNode(node, data, rotateList=[]) {
    if (node === null) {
      return (new NodeAVL(data));
    }
    
    if (data < node.data) {
      node.left = this.insertNode(node.left, data, rotateList);
    } else if (data > node.data) {
      node.right = this.insertNode(node.right, data, rotateList);
    } 
    
    node.height = 1 + Math.max(this.getNodeHeight(node.left), this.getNodeHeight(node.right));
    
    let balanceFactor = this.getBalanceFactor(node);
    if (rotateList.length)
      rotateList[rotateList.length - 1].treeNodes = this.bfs(this.root)
    if (balanceFactor > MAX_RIGHT_OVERWEIGHT) {
      if (data < node.left.data) {
        rotateList.push({rotate:'right', balancingNodes:[node.data, node.left.data, node.left.left.data]})
        return this.rightRotate(node);
      } else if (data > node.left.data) {
        rotateList.push({rotate: 'left-right', balancingNodes:[node.data, node.left.data, node.left.right.data]})
        node.left = this.leftRotate(node.left);
        return this.rightRotate(node);
      }
    }
      
    if (balanceFactor < MAX_LEFT_OVERWEIGHT) {
      if (data > node.right.data) {
        rotateList.push({rotate:'left', balancingNodes:[node.data, node.right.data, node.right.right.data]})
        return this.leftRotate(node);
      } else if (data < node.right.data) {
        rotateList.push({rotate:'right-left', balancingNodes:[node.data, node.right.data, node.right.left.data]})
        node.right = this.rightRotate(node.right);
        return this.leftRotate(node);
      }
    }
    
    return node;
  }

  insert(data, rotateList=[]) {
      this.root = this.insertNode(this.root, data, rotateList);
  }


  removeNode(node, data, isMaxLeft=false, rotateList=[]) {
    if (node == null){
      return node;
    }

    if (data < node.data) {
      node.left = this.removeNode(node.left, data, rotateList);
    } else if (data > node.data) {
      node.right = this.removeNode(node.right, data, rotateList);
    } else {
      if ((node.left === null) || (node.right === null)) {
          let temp = null;

          if (temp == node.left) {
              temp = node.right;
          } else {
              temp = node.left;
          }
          
          if (temp == null) {
              temp = node;
              node = null;
          } else {
              node = temp;
          }
      } else {
          if (isMaxLeft) {
            let temp = this.maxNode(node.left);
            node.data = temp.data;
            node.left = this.removeNode(node.left, temp.data, isMaxLeft, rotateList);
          } else {
            let temp = this.minNode(node.right);
            node.data = temp.data;
            node.right = this.removeNode(node.right, temp.data, isMaxLeft, rotateList);
          }
      }
    }
    if (node == null) {
      return node;
    }

    node.height = Math.max(this.getNodeHeight(node.left), this.getNodeHeight(node.right)) + 1;
    let balanceFactor = this.getBalanceFactor(node);
    if (rotateList.length)
        rotateList[rotateList.length - 1].treeNodes = this.bfs(this.root)
      
    if (balanceFactor > MAX_RIGHT_OVERWEIGHT) {
        if (this.getBalanceFactor(node.left) >= 0) {
            rotateList.push({rotate:'right', balancingNodes:[node.data, node.left.data, node.left.left.data]})
            return this.rightRotate(node);
        } else {
            rotateList.push({rotate: 'left-right', balancingNodes:[node.data, node.left.data, node.left.right.data]})
            node.left = this.leftRotate(node.left);
            return this.rightRotate(node);
        }
    } else if (balanceFactor < MAX_LEFT_OVERWEIGHT) {
        if (this.getBalanceFactor(node.right) <= 0) {
            rotateList.push({rotate:'left', balancingNodes:[node.data, node.right.data, node.right.right.data]})
            return this.leftRotate(node);
        } else {
            rotateList.push({rotate:'right-left', balancingNodes:[node.data, node.right.data, node.right.left.data]})
            node.right = this.rightRotate(node.right);
            return this.leftRotate(node);
        }
    }

    return node;
  }
      

  remove(data, isMaxLeft=false, rotateList=[]) {
      this.root = this.removeNode(this.root, data, isMaxLeft, rotateList);
  }
}