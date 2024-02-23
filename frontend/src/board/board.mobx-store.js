import {observable, runInAction} from "mobx";


export default class BoardStore {
    @observable accessor selectedClueIndex = 0;

    constructor(crossword) {
        this.crossword = crossword;
    }

    setupClueIndex(clueIndex) {
        runInAction(() => {
            this.selectedClueIndex = clueIndex;
        })
    }
}