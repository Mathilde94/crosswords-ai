export const DIRECTIONS = {
    VERTICAL: 'VERTICAL',
    HORIZONTAL: 'HORIZONTAL'
};

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
        this.content = props.content
        this.globalIndex = props.globalIndex
    }
}

export default class Crossword {
    constructor(matrix, clues, id) {
        this.matrix = matrix;
        this.clues = clues;
        this.id = id
    }

    fetchPositionsForClue(clue) {
        const initialPosition = clue.position
        const direction = clue.position.direction
        let path = []
        for (let index = 0; index < clue.length; index ++) {
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

    getHorizontalClues() {
        return this.clues.filter((clue) => clue.position.direction[1] === 1)
    }

    getVerticalClues() {
        return this.clues.filter((clue) => clue.position.direction[1] === 0)
    }
}