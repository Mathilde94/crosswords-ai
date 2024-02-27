import React, {Component} from 'react';
import {observer} from 'mobx-react';
import BoardStore from "./board.mobx-store";
import {action, runInAction} from "mobx";

import './styles.css';


@observer
export default class BoardReactComponent extends Component {
    constructor(props) {
        super(props);
        this.store = new BoardStore(this.props.crossword);
    }

    renderCell(cell, rowIndex, columnIndex) {
        let cellStyle = this.store.isCellFromSelectedClue(rowIndex, columnIndex) ? "selected" : (
            this.store.isCellEmpty(cell) ? "empty" : ""
        );
        const beginningClues = this.store.getBeginningCluesIndexes(rowIndex, columnIndex);
        return <div key={rowIndex * 100 + columnIndex} className={`cell ${cellStyle}`} onClick={() => beginningClues && this.updateSelectedClue(beginningClues[0])}>
            <span className={"cell-content"}>{cell}</span>
            {beginningClues && <span className="beginning-clues">
                {beginningClues.map(clue => clue.globalIndex).join(",")}
            </span>}
        </div>
    }

    renderRow(row, rowIndex) {
        return (<div className="row">
            {row.map((cell, columnIndex) => (<div>
                {this.renderCell(cell, rowIndex, columnIndex)}
            </div>))}
        </div>)
    }

    renderClue(clueIndex, clue) {
        const clueStyle = clue === this.store.selectedClue ? "selected" : "";
        return (
            <div className={`clue ${clueStyle}`} key={clueIndex} onClick={() => this.updateSelectedClue(clue)}>
                <span className="clue-global-index">{clue.globalIndex}</span>
                <span>{clue.clue}</span>
            </div>
        )
    }

    @action
    updateSelectedClue = (clue) => {
        return runInAction(() => {
            this.store.setupSelectedClue(clue)
        });
    }

    renderHorizontalClues() {
        return (<div>
            <span className="clue-type">Horizontal</span>
            {this.props.crossword.getHorizontalClues().map((clue, clueIndex) => (
                <div>{this.renderClue(clueIndex, clue)}</div>
            ))}
        </div>)
    }

    renderVerticalClues() {
        return (<div>
            <span className="clue-type">Vertical</span>
            {this.props.crossword.getVerticalClues().map((clue, clueIndex) => (
                <div>{this.renderClue(clueIndex, clue)}</div>
            ))}
        </div>)
    }

    renderClues() {
        return (
            <div className="clues">
                {this.renderHorizontalClues()}
                {this.renderVerticalClues()}
            </div>
        )
    }

    render() {
        const {crossword} = this.props
        return (
            <div className="board">
                <div className="clueContainer">{this.renderClues()}</div>
                <div className="matrix">
                    {crossword.matrix.map((row, rowIndex) => (<div key={rowIndex}>
                        {this.renderRow(row, rowIndex)}
                    </div>))}
                </div>
            </div>
        )
    }
}