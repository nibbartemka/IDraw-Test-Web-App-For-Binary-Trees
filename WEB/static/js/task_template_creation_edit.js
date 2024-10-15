// НИНАДА ЮРиСДИКЦИЯ АРТЁМА



const nodeCountElementName = "tree_template_keys_amount";
const nodeCountElement = document.querySelector(`input[name=${nodeCountElementName}]`);
const treeHeightName = "tree_template_height";
const treeHeightElement = document.querySelector(`input[name=${treeHeightName}]`);
const treeDivName = "tree"
const treeDivElement = document.querySelector(`div[name=${treeDivName}]`);
const treeTypeName = "tree_type_id"
const treeTypeElement = document.querySelector(`input[name=${treeTypeName}]`);
const keyTypeName = "key_template_id"
const keyTypeElement = document.querySelector(`input[name=${keyTypeName}]`);
const treeStructureName = "tree_structure"
const treeStructureElement = document.querySelector(`input[name=${treeStructureName}]`)
const difficultyName = 'diffuculty'
const difficultyElement = document.querySelector(`div[name=${difficultyName}]`)
const operationName = "operation_template_id"
const operationElement = document.querySelector(`select[name=${operationName}]`);
const operationTextName = 'operation_text'
const operationTextElement = document.querySelector(`div[name=${operationTextName}]`)
const nodeIndexName = 'node_index'
const nodeIndexElement = document.querySelector(`input[name=${nodeIndexName}]`)
const separator = ';'

const alphabet = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x',
    'y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
]

const MAX_INT = 100

const data_operations = {
    1: 'Выполните обход дерева в глубину', // БДП
    2: 'Выполните обход дерева в глубину', // АВЛ
    3: 'Выполните обход дерева в ширину', // БДП
    4: 'Выполните обход дерева в ширину', // АВЛ
    5: 'Выполните добавление узла', // с повторением слева БДП
    6: 'Выполните добавление узла', // с повторением справа БДП
    7: 'Выполните добавление узла', // без повторения слева БДП
    8: 'Выполните добавление узла', // без повторения справа БДП
    9: 'Выполните добавление узла', // добавление слева АВЛ
    10: 'Выполните добавление узла', // добавление справа АВЛ
    11: 'Выполните удаление узла', // удаление в БДП с заменой на мин. справа
    12: 'Выполните удаление узла', // удаление в БДП с заменой на макс. слева
    13: 'Выполните удаление узла', // удаление в АВЛ с заменой на мин. справа
    14: 'Выполните удаление узла' // удаление в АВЛ с заменой на макс. слева
}


function getNodesAddToLeft(treeValues) {
    let result = {}

    for (let i in treeValues) {
        if ((treeValues[i] !== undefined) && (treeValues[2 * i + 1] === undefined)) {
            result[treeValues[i]] = 2 * i + 1
        }
    }

    return result
}

function getNodesAddToRight(treeValues) {
    let result = {}

    for (let i in treeValues) {
        if ((treeValues[i] !== undefined) && (treeValues[2 * i + 2] === undefined)) {
            result[treeValues[i]] = 2 * i + 2
        }
    }

    return result
}

function updateDifficultyBlock(difficultyElement, operationValue, treeValues, nodeIndex, tempDifficulty) {
    if ([1, 2, 3, 4, 15, 16].includes(+operationValue)) {
        difficultyElement.innerHTML = `
            <label class='b_filter'>
                Сложность обхода: <br>
                <input class="input_text" type="number" name="task_template_difficulty" min="0.1" max="1.0" step="0.1" value='${tempDifficulty}' />
            </label>    
        `
    } else if (+operationValue >= 11) {
        difficultyElement.innerHTML = `
            <label class='b_filter'>
                Сложность удаления узла ${treeValues[+nodeIndex]}: <br>
                <input class="input_text" type="number" name="task_template_difficulty" min="0.1" max="1.0" step="0.1" value='${tempDifficulty}' />
            </label>
        `
    } else if ([5, 7, 9].includes(+operationValue)) {
        difficultyElement.innerHTML = `
            <label class='b_filter'>
                Сложность добавления узла к ${treeValues[Math.floor((nodeIndex - 1) / 2)]}: <br>
                <input class="input_text" type="number" name="task_template_difficulty" min="0.1" max="1.0" step="0.1" value='${tempDifficulty}' />
            </label>
        `
    } else {
        difficultyElement.innerHTML = `
        <label class='b_filter'>
            Сложность добавления узла к ${treeValues[Math.floor((nodeIndex - 1) / 2)]}: <br>
            <input class="input_text" type="number" name="task_template_difficulty" min="0.1" max="1.0" step="0.1" value='${tempDifficulty}' />
        </label>
        `
    }
}


function getTree(treeType) {
    if (treeType == 1) { // БДП
        return new BinarySearchTree()
    } else if (treeType == 2) { // АВЛ
        return new AVLTree()
    }
}

function fillTree(tree, valueList) {
    if (valueList.length == 0) {
        return;
    }
    
    tree.freeMemory();
    Array.from(valueList).forEach(element => {
        if (element !== undefined) {
            tree.insert(element)
        }
    });

    treeDivElement.innerHTML = tree.treePrinter()
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
let operationValue = operationElement.value;
let nodeIndex = nodeIndexElement.value;
let tempDifficulty = document.querySelector(`input[name='temp_difficulty']`).value
let treeValues = []


do {
    treeValues = getTreeValuesFromStructure(keyTypeValue)
    fillTree(
        tree, 
        treeValues
    );
} while (tree.height(tree.root) !== treeHeight || hasDuplicates(treeValues))
updateDifficultyBlock(difficultyElement, operationValue, treeValues, nodeIndex, tempDifficulty)

