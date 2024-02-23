import React, {Component} from 'react';
import {observer} from 'mobx-react';
import './style.css';
import CrosswordStore from "./crossword.mobx-store";
import BoardReactComponent from "../board/board.react-component";
import {action} from "mobx";

@observer
export default class CrosswordReactComponent extends Component {

    constructor(props) {
        super(props);
        const urlSearchString = window.location.search;
        const params = new URLSearchParams(urlSearchString);
        this.crosswordId = params.get("crosswordId");
        this.store = new CrosswordStore(this.crosswordId);
    }

    componentDidMount() {
        if (this.crosswordId) {
            this.store.loadCrossword();
        }
    }

    @action
    createNewCrossword() {
        this.store.createNewCrossword().then((crossword) => {
            this.store.loadCrossword()
        })
    }

    render() {
        if (!this.store.isLoaded && !this.store.crosswordId) {
            return (<div>
                <span>Feeling lucky? Create a new crossword here:</span>
                <button onClick={() => this.createNewCrossword()}>Create new crossword</button>
            </div>)
        }
        if (!this.store.isLoaded || this.store.crossword === null) {
            return (<p>Loading the crossword...</p>)
        }
        return (
            <div className="container">
                <h1>Crossword</h1>
                <BoardReactComponent crossword={this.store.crossword} />
            </div>
        )
    }
}