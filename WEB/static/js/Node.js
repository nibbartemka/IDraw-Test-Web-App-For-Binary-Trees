class NodeBase {
    constructor(data) {
        this.data = data;
        this.left = null;
        this.right = null;
    };
};

class NodeBST extends NodeBase {
    constructor(data) {
        super(data);
    };
};

class NodeAVL extends NodeBase {
    constructor(data) {
        super(data);
        this.height = 1;
    };
}