import axios from "axios";
import {runInAction, observable, action} from 'mobx';

import {API_HOST_URL} from './constants'
import Crossword, {Clue, Position} from "./model";

export default class CrosswordStore {
    @observable accessor isLoaded = false;
    @observable accessor crossword = null;

    constructor(crosswordId ) {
        this.crosswordId = crosswordId;
    }

    @action
    setupCrossword(crossword) {
        this.crossword = crossword;
    }

    setupLoadedState(loaded) {
        runInAction(() => {
            this.isLoaded = loaded;
        })
    }

    createCrosswordFromData(data) {
        const uniqueClues = {}
        let allClues = []
        data.data.clues.forEach((clue) => {
            if (uniqueClues[clue.clue] === undefined) {
                uniqueClues[clue.clue] = clue.clue
                if (clue.word in data.data.board.words_position) {
                    allClues = allClues.concat([new Clue({
                        clue: clue.clue,
                        position: new Position({
                            row: data.data.board.words_position[clue.word][0][0],
                            column: data.data.board.words_position[clue.word][0][1],
                            direction: data.data.board.words_position[clue.word][1],
                        }),
                        length: clue.word.length,
                        // TODO: remove later
                        content: clue.word
                    })])
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
                this.isLoaded = true;
                this.setupCrossword(this.createCrosswordFromData(data));
            });
        }
    }

    @action
    async createNewCrossword() {
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
        return this.crossword
    }
}