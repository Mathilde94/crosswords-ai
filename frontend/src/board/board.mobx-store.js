import {observable, runInAction} from "mobx";

const EMPTY_CELL = ". ";

export default class BoardStore {
    @observable accessor selectedClue = null;

    constructor(crossword) {
        this.crossword = crossword;
    }

    setupSelectedClue(clue) {
        runInAction(() => {
            this.selectedClue = clue;
        })
    }

    isCellFromSelectedClue(rowIndex, columnIndex) {
        if (!this.selectedClue) {
            return false;
        }
        const positions = this.crossword.fetchPositionsForClue(this.selectedClue);
        for (const positionIndex in positions) {
            if (positions[positionIndex].row === rowIndex && positions[positionIndex].column === columnIndex) {
                return true;
            }
        }
        return false;
    }

    getBeginningCluesIndexes(rowIndex, columnIndex) {
        // return all the clues that start at this cell for markers in cell
        return this.crossword.clues.filter((clue) =>
            clue.position.row === rowIndex && clue.position.column === columnIndex
        )
    }

    isCellEmpty(cell) {
        return cell === EMPTY_CELL;
    }
}