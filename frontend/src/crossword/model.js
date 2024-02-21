export default class Crossword {
    constructor(crosswordId, matrix, clues, wordsPositions) {
        this.crosswordId = crosswordId;
        this.matrix = matrix;
        this.clues = clues;
        this.wordsPositions = wordsPositions;
    }
}