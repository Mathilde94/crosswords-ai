import axios from "axios";
import {runInAction, observable, action, computed} from 'mobx';

import {API_HOST_URL, STATES} from './constants'
import Crossword, {Clue, Position} from "./models";

export default class CrosswordStore {
    @observable accessor crossword = null;
    @observable accessor state = STATES.INIT;

    constructor(crosswordId ) {
        this.crosswordId = crosswordId;
    }

    @computed
    get isLoaded() {
        return this.crossword !== null;
    }

    @action
    setupCrossword(crossword) {
        this.crossword = crossword;
    }
    createCrosswordFromData(data) {
        const uniqueClues = {}
        let allClues = []
        let globalIndex = 1
        data.data.clues.forEach((clue, index) => {
            if (uniqueClues[clue.clue] === undefined) {
                uniqueClues[clue.clue] = clue.clue
                if (clue.word in data.data.board.words_position) {
                    const wordPositions = data.data.board.words_position[clue.word];
                    allClues = allClues.concat([new Clue({
                        clue: clue.clue,
                        position: new Position({
                            row: wordPositions[0][0],
                            column: wordPositions[0][1],
                            direction: wordPositions[1],
                        }),
                        length: clue.word.length,
                        word: clue.word,
                        globalIndex,
                    })])
                    globalIndex ++;
                }
            }
        });
        return new Crossword(data.data.board.matrix, allClues, data.data.id)
    }

    @action
    async loadCrossword() {
        const data = await axios.get(
            `${API_HOST_URL}/crosswords/?crossword_id=${this.crosswordId}`,
            {
                headers: {
                    'Content-Type': 'application/json',
                }
            }
        );
        if (data.data.status !== "completed") {
            setTimeout(() => {
                this.loadCrossword()
            }, 1000)
        } else {
            runInAction(() => {
                this.setupCrossword(this.createCrosswordFromData(data));
            });
        }
    }

    @action
    setupState(state) {
        runInAction(() => {
            this.state = state;
        })
    }

    @action
    async createNewCrossword() {
        runInAction(() => {
            this.state = STATES.LOADING
        });
        const data = await axios.post(
            `${API_HOST_URL}/crosswords/feeling_lucky/`,
            {
                headers: {
                    'Content-Type': 'application/json',
                }
            }
        );
        runInAction(() => {
            this.crosswordId = data.data.id;
        });
    }
}