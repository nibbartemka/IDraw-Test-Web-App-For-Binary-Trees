const nodeCountElementName = "node_count";
const nodeCountElement = document.querySelector(`input[name=${nodeCountElementName}]`);
const treeHeightName = "tree_height";
const treeHeightElement = document.querySelector(`input[name=${treeHeightName}]`);
const treeDivName = "tree"
const treeDivElement = document.querySelector(`div[name=${treeDivName}]`);
const treeTypeName = "tree_type_id"
const treeTypeElement = document.querySelector(`select[name=${treeTypeName}]`);
const keyTypeName = "key_template_id"
const keyTypeElement = document.querySelector(`select[name=${keyTypeName}]`);
const treeStructureName = "tree_structure"
const treeStructureElement = document.querySelector(`input[name=${treeStructureName}]`)
const separator = ';'

const alphabet = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x',
    'y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
]

const MAX_INT = 100

function getTree(treeType) {
    if (treeType == 1) { // БДП
        return new BinarySearchTree()
    } else if (treeType == 2) { // АВЛ
        return new AVLTree()
    }
}
// мб нинада
// function findMinimum(arr) {
//     const validValues = arr.filter(value => typeof value === 'number');
  
//     if (validValues.length === 0) {
//         return undefined;
//     }

//     return Math.min(...validValues);
// }

// function getList(list, treeHeight) {
//     let result = list.filter((x) => x < (Math.pow(2, treeHeight - 2) - 1))

//     console.log(result)
//     let temp = list.filter((x) => x >= (Math.pow(2, treeHeight - 2) - 1))
//     let i = 0
//     let j = temp.length - 1

//     while (i <= j) {
//         if (i === j) {
//             result.push(temp[i++])
//             continue
//         }
//         result.push(temp[j--])
//         result.push(temp[i++])
//     }

//     return result
// }

function helper(list) {
    let result = list.filter((x) => x % 2 === list[0] % 2)
    if (Math.floor(Math.random() * 2)) {
        result.push.apply(result, list.filter((x) => x % 2 !== list[0] % 2))
    } else {
        result.push.apply(result, list.filter((x) => x % 2 !== list[0] % 2).reverse())
    }
    
    return result
}

function getList(list, treeHeight) {
    let firstPart = list.filter((x) => x < Math.pow(2, treeHeight - 2) - 1)
    let secondPart = list.filter(
        (x) => x >= Math.pow(2, treeHeight - 2) - 1 && x < Math.pow(2, treeHeight - 1) - 1
    )
    let thirdPart = list.filter(
        (x) => x >= Math.pow(2, treeHeight - 1) - 1
    )

    firstPart.push.apply(firstPart, helper(secondPart))
    firstPart.push.apply(firstPart, thirdPart)

    return firstPart
}

function generateNumValues(height, nodeCount) {
    if (!(height && nodeCount)) {
        return []
    }

    let maxNodes = Math.pow(2, height) - 1
    let arr = [...Array(maxNodes)]
    
    arr[0] = Math.floor(Math.random() * MAX_INT) + 60
    
    let prev_index = 0
    let cur_index = 2 * prev_index + 1 + Math.floor(Math.random() * 2);

    while (cur_index < maxNodes) {
        let head_index = prev_index
        is_odd = head_index % 2

        if (prev_index % 2 == cur_index % 2) {
            while (head_index > 0 && head_index % 2 == is_odd) {
                head_index = Math.floor((head_index - 1) / 2)
            }
        }
        else {
            temp = Math.floor((head_index - 1) / 2)
            head_index = (temp < 0) ? 0 : temp
        }
        
        if (head_index < 0) {
            head_index = 0
        } else {
            if (cur_index % 2 == prev_index % 2) {
                temp = Math.floor((head_index - 1) / 2)
                head_index = (temp < 0) ? 0 : temp
            }
        }
        
        if (prev_index == head_index) {
            if (cur_index % 2) {
                cur_value = Math.floor(Math.random() * arr[prev_index])
            } else {
                cur_value = Math.floor(Math.random() * MAX_INT) + arr[prev_index]
            }
        } else {
            if (cur_index % 2 == 0 && prev_index % 2 == 1) {
                cur_value = Math.floor(Math.random() * (arr[head_index] - arr[prev_index])) + arr[prev_index]
            } else if (cur_index % 2 == 1 && prev_index % 2 == 0) {
                cur_value = Math.floor(Math.random() * (arr[prev_index] - arr[head_index])) + arr[head_index]
            } else if (cur_index % 2 == 1 && prev_index % 2 == 1) {
                temp_runner = cur_index
                temp_is_odd = temp_runner % 2
                flag = false
                while (!flag && temp_runner > 0) {
                    if (temp_runner % 2 != temp_is_odd)
                        flag = true
                    temp_runner = Math.floor((temp_runner - 1) / 2)
                }
                if (flag)
                     cur_value = Math.floor(Math.random() * (arr[prev_index] - arr[head_index])) + arr[head_index]
                else
                    cur_value = Math.floor(Math.random() * (arr[prev_index]))
            } else {
                temp_runner = cur_index
                temp_is_odd = temp_runner % 2
                flag = false
                while (!flag && temp_runner > 0) {
                    if (temp_runner % 2 != temp_is_odd)
                        flag = true
                    temp_runner =  Math.floor((temp_runner - 1) / 2)
                }
                if (flag)
                    cur_value = Math.floor(Math.random() * (arr[head_index] - arr[prev_index])) + arr[prev_index]
                else
                    cur_value = Math.floor(Math.random() * (MAX_INT)) + arr[prev_index]
            }
        }

        arr[cur_index] = cur_value  
        prev_index = cur_index
        cur_index = 2 * prev_index + 1 + Math.floor(Math.random() * 2);
    }
    
    
    empty_indexes = []
    for (let index = 0; index < nodeCount; index++) {
        if (arr[index] === undefined) {
            empty_indexes.push(index)
        }
    }
    empty_indexes = getList(empty_indexes, height)
    // console.log(empty_indexes)
    empty_indexes = empty_indexes.splice(0, nodeCount - height)
    // console.log(empty_indexes)

    for (let i in empty_indexes) {
        let cur_index = empty_indexes[i];
        let prev_index = Math.floor((cur_index - 1) / 2)
        head_index = prev_index
        is_odd = head_index % 2
    
        if (prev_index % 2 == cur_index % 2) {
            while (head_index > 0 && head_index % 2 == is_odd) {
                head_index = Math.floor((head_index - 1) / 2)
            }
        }
        else {
            temp = Math.floor((head_index - 1) / 2)
            head_index = (temp < 0) ? 0 : temp
        }
        
        if (head_index < 0) {
            head_index = 0
        } else {
            if (cur_index % 2 == prev_index % 2) {
                temp = Math.floor((head_index - 1) / 2)
                head_index = (temp < 0) ? 0 : temp
            }
        }
        
        if (prev_index == head_index) {
            if (cur_index % 2) {
                cur_value = Math.floor(Math.random() * arr[prev_index])
            } else {
                cur_value = Math.floor(Math.random() * MAX_INT) + arr[prev_index]
            }
        } else {
            if (cur_index % 2 == 0 && prev_index % 2 == 1) {
                cur_value = Math.floor(Math.random() * (arr[head_index] - arr[prev_index])) + arr[prev_index]
            } else if (cur_index % 2 == 1 && prev_index % 2 == 0) {
                cur_value = Math.floor(Math.random() * (arr[prev_index] - arr[head_index])) + arr[head_index]
            } else if (cur_index % 2 == 1 && prev_index % 2 == 1) {
                temp_runner = cur_index
                temp_is_odd = temp_runner % 2
                flag = false
                while (!flag && temp_runner > 0) {
                    if (temp_runner % 2 != temp_is_odd)
                        flag = true
                    temp_runner =  Math.floor((temp_runner - 1) / 2)
                }
                if (flag)
                     cur_value = Math.floor(Math.random() * (arr[prev_index] - arr[head_index])) + arr[head_index]
                else
                    cur_value = Math.floor(Math.random() * (arr[prev_index]))
            } else {
                temp_runner = cur_index
                temp_is_odd = temp_runner % 2
                flag = false
                while (!flag && temp_runner > 0) {
                    if (temp_runner % 2 != temp_is_odd)
                        flag = true
                    temp_runner =  Math.floor((temp_runner - 1) / 2)
                }
                if (flag)
                    cur_value = Math.floor(Math.random() * (arr[head_index] - arr[prev_index])) + arr[prev_index]
                else
                    cur_value = Math.floor(Math.random() * (MAX_INT)) + arr[prev_index]
            }
        }

        arr[cur_index] = cur_value

        prev_index = cur_index
        cur_index = 2 * prev_index + 1 + Math.floor(Math.random() * 2);
    }
    
    return arr
}


function generateStrValues(height, nodeCount) {
    let res = generateNumValues(height, nodeCount);

    return res.map(function(item) {
        if (item === undefined){
            return item
        }

        first_letter_index = Math.floor(item / 10)
        second_letter_index = item % 10
        return alphabet[first_letter_index] + alphabet[second_letter_index];
    })
}


function getTreeValues(keyType, height, nodeCount) {
    if (keyType == 1) { // Числовой
        return generateNumValues(height, nodeCount)
    } else if (keyType == 2) { // Строковый
        return generateStrValues(height, nodeCount)
    }
}


function fillTree(tree, valueList) {
    if (valueList.length == 0) {
        return;
    }
    // console.log(valueList)
    tree.freeMemory();
    Array.from(valueList).forEach(element => {
        if (element !== undefined) {
            tree.insert(element)
        }
    });
    
    treeDivElement.innerHTML = tree.treePrinter()
}


minValueAVL = {
    3: 4,
    4: 7,
    5: 12,
}

function updateNodeCountElement(nodeCountElement, treeTypeValue, treeHeight) {
    if (treeTypeValue == 1) { // БДП 
        nodeCountElement.min = treeHeight
    } else {
        // nodeCountElement.min = Math.pow(2, treeHeight - 1);
        nodeCountElement.min = minValueAVL[+treeHeight]
    }
    nodeCountElement.max = Math.pow(2, treeHeight) - 1;

    if (+nodeCountElement.value < nodeCountElement.min) {
        nodeCountElement.value = nodeCountElement.min
    }

    if (+nodeCountElement.value > nodeCountElement.max) {
        nodeCountElement.value = nodeCountElement.max
    }
}


function getTreeSctructure(treeValues) {
    if (!treeValues) {
        return ""
    }

    return treeValues.map(item => (typeof item !== 'undefined') ? '1' : '0').join('');
}


function updateTreeStructure(treeStructureElement, treeValues) {
    treeStructureElement.value = getTreeSctructure(treeValues)
}


function generateNumValuesFromStructure(list) {
    if (!list) {
        return []
    }

    let maxNodes = list.length
    let arr = [...list]
    arr[0] = Math.floor(Math.random() * MAX_INT) + 20
    
    empty_indexes = []
    for (let index = 1; index < maxNodes; index++) {
        if (arr[index]) {
            empty_indexes.push(index)
        }
    }
    
    for (let i in empty_indexes) {
        let cur_index = empty_indexes[i];
        let prev_index = Math.floor((cur_index - 1) / 2)
        head_index = prev_index
        is_odd = head_index % 2
    
        if (prev_index % 2 == cur_index % 2) {
            while (head_index > 0 && head_index % 2 == is_odd) {
                head_index = Math.floor((head_index - 1) / 2)
            }
        }
        else {
            temp = Math.floor((head_index - 1) / 2)
            head_index = (temp < 0) ? 0 : temp
        }
        
        if (head_index < 0) {
            head_index = 0
        } else {
            if (cur_index % 2 == prev_index % 2) {
                temp = Math.floor((head_index - 1) / 2)
                head_index = (temp < 0) ? 0 : temp
            }
        }
        
        if (prev_index == head_index) {
            if (cur_index % 2) {
                cur_value = Math.floor(Math.random() * arr[prev_index])
            } else {
                cur_value = Math.floor(Math.random() * MAX_INT) + arr[prev_index]
            }
        } else {
            if (cur_index % 2 == 0 && prev_index % 2 == 1) {
                cur_value = Math.floor(Math.random() * (arr[head_index] - arr[prev_index])) + arr[prev_index]
            } else if (cur_index % 2 == 1 && prev_index % 2 == 0) {
                cur_value = Math.floor(Math.random() * (arr[prev_index] - arr[head_index])) + arr[head_index]
            } else if (cur_index % 2 == 1 && prev_index % 2 == 1) {
                temp_runner = cur_index
                temp_is_odd = temp_runner % 2
                flag = false
                while (!flag && temp_runner > 0) {
                    if (temp_runner % 2 != temp_is_odd)
                        flag = true
                    temp_runner =  Math.floor((temp_runner - 1) / 2)
                }
                if (flag)
                     cur_value = Math.floor(Math.random() * (arr[prev_index] - arr[head_index])) + arr[head_index]
                else
                    cur_value = Math.floor(Math.random() * (arr[prev_index]))
            } else {
                temp_runner = cur_index
                temp_is_odd = temp_runner % 2
                flag = false
                while (!flag && temp_runner > 0) {
                    if (temp_runner % 2 != temp_is_odd)
                        flag = true
                    temp_runner =  Math.floor((temp_runner - 1) / 2)
                }
                if (flag)
                    cur_value = Math.floor(Math.random() * (arr[head_index] - arr[prev_index])) + arr[prev_index]
                else
                    cur_value = Math.floor(Math.random() * (MAX_INT)) + arr[prev_index]
            }
        }

        arr[cur_index] = cur_value
    
        prev_index = cur_index
        cur_index = 2 * prev_index + 1 + Math.floor(Math.random() * 2);
    }
    return arr
}


function getTreeValuesFromStructure(keyTypeValue) {
    treeValues = generateNumValuesFromStructure(treeStructureElement.value.split('').map(function(x) {
        if (parseInt(x)) {
            return x;
        }
    }))

    if (keyTypeValue == 2) { // Строковый
        treeValues = treeValues.map(function(item) {
            if (item === undefined){
                return item
            }
    
            first_letter_index = Math.floor(item / 10)
            second_letter_index = item % 10
            return alphabet[first_letter_index] + alphabet[second_letter_index];
        })
    }

    return treeValues;
}

function hasDuplicates(arr) {
    let filteredArray = arr.filter(value => value !== undefined);
    let uniqueValues = new Set(filteredArray);
  
    return filteredArray.length !== uniqueValues.size;
}


let treeTypeValue = treeTypeElement.value;
let tree = getTree(treeTypeValue);
let keyTypeValue = keyTypeElement.value;
let nodeCount = (nodeCountElement.value) ? +nodeCountElement.value : 0;
let treeHeight = (treeHeightElement.value) ? +treeHeightElement.value : 0;
let treeValues = []

updateNodeCountElement(nodeCountElement, treeTypeValue, treeHeight)
if (!treeStructureElement.value) {
    do {
        treeValues = getTreeValues(keyTypeValue, treeHeight, nodeCount)
        fillTree(
            tree, 
            treeValues
        );
    } while (tree.height(tree.root) !== treeHeight || hasDuplicates(treeValues))
} else {
    do {
        treeValues = getTreeValuesFromStructure(keyTypeValue)
        fillTree(
            tree, 
            treeValues
        );
    } while (tree.height(tree.root) !== treeHeight || hasDuplicates(treeValues))
}
updateTreeStructure(treeStructureElement, treeValues)


keyTypeElement.addEventListener('change', function() {
    keyTypeValue = keyTypeElement.value;

    if (!treeStructureElement.value) {
        do {
            treeValues = getTreeValues(keyTypeValue, treeHeight, nodeCount)
            fillTree(
                tree, 
                treeValues
            );
        } while (tree.height(tree.root) !== treeHeight || hasDuplicates(treeValues))
    } else {
        do {
            treeValues = getTreeValuesFromStructure(keyTypeValue)
            fillTree(
                tree, 
                treeValues
            );
        } while (tree.height(tree.root) !== treeHeight || hasDuplicates(treeValues))
    }
    updateTreeStructure(treeStructureElement, treeValues)
});


treeTypeElement.addEventListener('change', function() {
    treeTypeValue = treeTypeElement.value;
    tree = getTree(treeTypeValue)

    updateNodeCountElement(nodeCountElement, treeTypeValue, treeHeight)

    nodeCount = +nodeCountElement.value;
    do {
        treeValues = getTreeValues(keyTypeValue, treeHeight, nodeCount)
        fillTree(
            tree, 
            treeValues
        );
    } while (tree.height(tree.root) !== treeHeight || hasDuplicates(treeValues))
    updateTreeStructure(treeStructureElement, treeValues)
})


treeHeightElement.addEventListener('change', function() {
    if (this.value < 3) {
        this.value = 3
    } else if (this.value > 5) {
        this.value = 5
    }
    treeHeight = +treeHeightElement.value;

    updateNodeCountElement(nodeCountElement, treeTypeValue, treeHeight)
    
    nodeCount = +nodeCountElement.value;
    do {
        treeValues = getTreeValues(keyTypeValue, treeHeight, nodeCount);
        fillTree(
            tree, 
            treeValues
        );
    } while (tree.height(tree.root) !== treeHeight || hasDuplicates(treeValues))
    updateTreeStructure(treeStructureElement, treeValues)
})


nodeCountElement.addEventListener('change', function() {
    if (+this.value < +this.min) {
        this.value = +this.min
    } else if (+this.value > +this.max) {
        this.value = +this.max
    }
    nodeCount = +nodeCountElement.value;
    do {
        treeValues = getTreeValues(keyTypeValue, treeHeight, nodeCount);
        fillTree(
            tree, 
            treeValues
        );
    } while (tree.height(tree.root) !== treeHeight || hasDuplicates(treeValues));
    updateTreeStructure(treeStructureElement, treeValues)
})