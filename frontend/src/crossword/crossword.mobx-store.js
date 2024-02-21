import axios from "axios";
import {runInAction, observable, action} from 'mobx';

import {API_HOST_URL} from './constants'
import Crossword from "./model";

export default class CrosswordStore {
    @observable accessor isLoaded = false;
    @observable accessor crossword = null;

    constructor(crosswordId ) {
        this.crosswordId = crosswordId;
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
        // need to fetch unique clue
        const clues = {}
        data.data.clues.forEach((clue) => {
            if (clues[clue.word] === undefined) {
                clues[clue.word] = clue.clue
            }
        });
        runInAction(() => {
            this.isLoaded = true;
            this.crossword = new Crossword(
                this.crosswordId,
                data.data.board.matrix,
                clues,
                data.data.board.words_position
            );
        });
    }
}