class TreeBase {
    constructor() {
        this.root = null;
    }

    insert(data) {
        console.log("Need to override")
    }

    search(data) {
        if (this.root === null) {
            return null;
        } else {
            return this.searchNode(this.root, data);
        };
    }

    searchNode(node, data) {
        if (data === node.data) {
            return node;
        } else if (data < node.data){
            if (node.left === null) {
                return null;
            } else {
                return this.searchNode(node.left, data);
            };
        } else {
            if (node.right === null) {
                return null;
            } else {
                return this.searchNode(node.right, data);
            };
        }
    }

    minNode(node) {
        if (node.left === null)
            return node;
        else
            return this.minNode(node.left);
    }

    maxNode(node) {
        if (node.right === null)
            return node;
        else
            return this.maxNode(node.right);
    }

    remove(data) {
        console.log("Need to override")
    }

    preorderTraversal(root, list = []) {
        if (!root) {
            return list;
        }
    
        list.push(root.data);
        this.preorderTraversal(root.left, list);
        this.preorderTraversal(root.right, list);
        
        return list;
    }

    // inorderTraversal(root, list=[]) {
    //     if (!root) {
    //         return list;
    //     }
        
    //     this.inorderTraversal(root.left, list);
    //     list.push(root.data);
    //     this.inorderTraversal(root.right, list);
    // }

    inorderTraversal(root) {
        let res = [];
        this.inorderTraversalHelper(root, res);
        return res;
    }
      
    inorderTraversalHelper(root, res) {
        if (!root) {
          return res;
        }
        this.inorderTraversalHelper(root.left, res);
        res.push(root.data);
        this.inorderTraversalHelper(root.right, res);
        return res;
    }

    postorderTraversal(root) {
        let res = [];
        this.postorderTraversalHelper(root, res);
        return res;
    }
      
    postorderTraversalHelper(root, res) {
        if (!root) {
          return res;
        }
        this.postorderTraversalHelper(root.left, res);
        this.postorderTraversalHelper(root.right, res);
        res.push(root.data);
        return res;
    }

    // postorderTraversal(root, list=[]) {
    //     if (!root) {
    //         return list;
    //     }
        
    //     this.postorderTraversal(root.left, list);
    //     this.postorderTraversal(root.right, list);
    //     list.push(root.data);
    // }

    _getMatrixWithBorders(M, height) {
        let rows = height;
        let columns = Math.pow(2, height) - 1
        // let columns = Math.pow(2, height) - 1 + Math.pow(2, height-1)

        for (let i = 0; i < rows - 2; i++) {
            let j = 0
            while (j < columns) {
                if (M[i][j] !== null) {
                    let leftBorder = (M[i + 1][j - Math.pow(2, height - 2 - i)] !== null) ? j - Math.pow(2, height - 2 - i) + 1 : j;
                    let rightBorder = (M[i + 1][j + Math.pow(2, height - 2 - i)] !== null) ? j + Math.pow(2, height - 2 - i) : j;
                    // let leftBorder = (M[i + 1][j - Math.pow(2, height - 2 - i) - 1] !== null) ? j - Math.pow(2, height - 2 - i) : j;
                    // let rightBorder = (M[i + 1][j + Math.pow(2, height - 2 - i) + 1] !== null) ? j + Math.pow(2, height - 2 - i) + 1 : j;
                    for (let z = leftBorder; z < rightBorder; z++) {
                        if (z === j) {
                            continue;
                        }
                        M[i][z] = '-'
                    }
                    // j = j + Math.pow(2, height - 2 - i);
                    j = j + Math.pow(2, height - 2 - i);
                } else {
                    j++;
                }
            }
        }
    }

    treePrinter() {
        if (!this.root) {
            return 
        }

        let res = "";

        const h = this.height(this.root);
        // const col = this.getCol(h) + Math.pow(2, h-1);
        const col = this.getCol(h + 1);
        const M = new Array(h).fill().map(() => new Array(col).fill(null));
        this.printTree(M, this.root, Math.floor(col / 2), 0, h + 1);
        this._getMatrixWithBorders(M, h + 1)
        // console.log(M)
        for (let i = 0; i < M.length; i++) { 
            let row='<div class="flex">';
            for (let j = 1; j < M[i].length - 1; j++) {
                if (M[i][j] === null) {
                    row = row + "<div class='empty-size'></div>";
                } else if (M[i][j] === '-') {
                    row = row + `<div class='empty-size border-bottom'></div>`
                } else {
                    // if (M.length - 1 == i) {
                    //     row= row + `
                    //     <div>
                    //         <hr width=100%>
                    //         <div class="size node" id=${M[i][j]} onclick="selectNode(this)">
                    //             ${M[i][j]}
                    //         </div>
                    //     </div>
                    // `;
                    // } else {
                        row= row + `
                            <div class="size node" id=${M[i][j]} onclick="selectNode(this)">
                                ${M[i][j]}
                            </div>
                    `;
                    // }
                }
            }
            row += "</div>";
            res += row;
        }
    
        return res
    };

    bfs() {
        let queue = [this.root];
        let result = [];
      
        while (queue.length > 0) {
          let currentNode = queue.shift();
          result.push(currentNode.data);
      
          if (currentNode.left) {
            queue.push(currentNode.left);
          }
          if (currentNode.right) {
            queue.push(currentNode.right);
          }
        }
      
        return result;
    }

    height(root) {
        if (root === null) {
            return 0;
        }
        return Math.max(this.height(root.left), this.height(root.right)) + 1;
    }
     
    getCol(h) {
        if (h === 1) {
            return 1;
        }
        return this.getCol(h - 1) + this.getCol(h - 1) + 1;
    }
     
    printTree(M, root, col, row, height) {
        if (root === null) {
            return;
        }
        M[row][col] = root.data;
        this.printTree(M, root.left, col - Math.pow(2, height - 2), row + 1, height - 1);
        this.printTree(M, root.right, col + Math.pow(2, height - 2), row + 1, height - 1);
        // this.printTree(M, root.left, Math.floor(col / 2), row + 1, height - 1);
        // this.printTree(M, root.right, Math.floor(col / 2) + Math.floor(Math.pow(2, height) - 1 + Math.pow(2, height-1) / 2), row + 1, height - 1);
    }

    freeMemory() {
        
        function getNodes(root, list=[]) {
            if (!root) {
                return list;
            }
        
            list.push(root);
            getNodes(root.left, list);
            getNodes(root.right, list);
            return list;
        }
        
        let nodeList = getNodes(this.root);
        this.root = null; 
        nodeList.map(function(node){
            node.left = null;
            node.right = null;
        });
    }
};