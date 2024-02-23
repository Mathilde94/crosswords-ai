import React, {Component} from 'react';
import {observer} from 'mobx-react';
import './styles.css';
import BoardStore from "./board.mobx-store";
import {action, runInAction} from "mobx";

@observer
export default class BoardReactComponent extends Component {
    constructor(props) {
        super(props);
        this.store = new BoardStore(this.props.crossword);
    }

    renderCell(cell, rowIndex, columnIndex) {
        const positions = this.props.crossword.fetchPositionsForClue(this.store.selectedClueIndex);
        for (const positionIndex in positions) {
            const position = positions[positionIndex];
            if (position.row === rowIndex && position.column === columnIndex) {
                return <span key={rowIndex * 100 + columnIndex} className="cell selected">{cell}</span>
            }
        }
        if (cell === ". ") {
            return <span key={rowIndex * 100 + columnIndex} className="cell empty">{""}</span>
        }
        return <span key={rowIndex * 100 + columnIndex} className="cell">{cell}</span>
    }

    renderRow(row, rowIndex) {
        return (<div className="row">
            {row.map((cell, columnIndex) => (<div>
                {this.renderCell(cell, rowIndex, columnIndex)}
            </div>
            ))}
        </div>)
    }

    renderClue(clueIndex) {
        const {clues} = this.props.crossword;
        const clue = clues[clueIndex]
        if (clueIndex === this.store.selectedClueIndex) {
            return (<span key={clueIndex} className="selected">{clue.clue}</span>);
        }
        return (<span key={clueIndex}>{clue.clue}</span>);
    }

    @action
    updateSelectedClue = (clueIndex) => {
        return runInAction(() => {
            this.store.setupClueIndex(clueIndex)
        });
    }

    renderClues() {
        const {crossword} = this.props
        return (
            <div className="clues">
                {Object.keys(crossword.clues).map((key, clueIndex) => (
                    <div key={clueIndex} onClick={() => this.updateSelectedClue(clueIndex)}>
                        {this.renderClue(clueIndex)}
                    </div>
                ))}
            </div>
        )
    }

    render() {
        const {crossword} = this.props
        return (
            <div className="board">
                <div>{this.renderClues()}</div>
                <div>
                    {crossword.matrix.map((row, rowIndex) => (<div key={rowIndex}>
                        {this.renderRow(row, rowIndex)}
                    </div>))}
                </div>
            </div>
        )
    }
}