import React, {Component} from 'react';
import {observer} from 'mobx-react';
import './styles.css';

@observer
export default class BoardReactComponent extends Component {
    constructor(props) {
        super(props);
    }

    renderCell(cell, index) {
        return <span key={index} className="cell">{cell}</span>
    }

    renderRow(index, row) {
        return (<div className="row">
            {row.map((cell, i) => (<div>
                {this.renderCell(cell, index * 10 + i)}
            </div>
            ))}
        </div>)
    }

    renderClues() {
        const {clues} = this.props.crossword
        return (
            <div className="clues">
                {Object.keys(clues).map((key, index) => (
                    <div key={index}>
                        {clues[key]}
                    </div>
                ))}
            </div>
        )
    }

    render() {
        const {matrix} = this.props.crossword
        return (
            <div className="board">
                <div>{this.renderClues()}</div>
                <div>
                    {matrix.map((row, index) => (<div key={index}>
                        {this.renderRow(index, row)}
                    </div>))}
                </div>
            </div>
        )
    }
}