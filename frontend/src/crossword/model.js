export class Position {
    constructor(props) {
        this.row = props.row
        this.column = props.column
        this.direction = props.direction
    }
}

export class Clue {
    constructor(props) {
        this.clue = props.clue
        this.position = props.position
        this.length = props.length
        // to remove later:
        this.content = props.content
    }
}

export default class Crossword {
    constructor(matrix, clues, id) {
        this.matrix = matrix;
        this.clues = clues;
        this.id = id
    }

    fetchPositionsForClue(clueIndex) {
        const clue = this.clues[clueIndex]
        const initialPosition = clue.position
        const direction = clue.position.direction
        let path = []
        for (let index = 0; index <= clue.length; index ++) {
            path = path.concat([
                new Position({
                    row: initialPosition.row + index * direction[0],
                    column: initialPosition.column + index * direction[1],
                    direction: clue.position.direction
                })
            ])
        }
        return path;
    }
}