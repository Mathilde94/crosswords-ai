import React, {Component} from 'react';
import {observer} from 'mobx-react';

import {action} from "mobx";
import { FidgetSpinner } from 'react-loader-spinner';

import CrosswordStore from "./crossword.mobx-store";
import BoardReactComponent from "../board/board.react-component";

import {STATES} from "./constants";
import './style.css';

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
            this.store.setupState(STATES.FETCHING)
            this.store.loadCrossword()
        })
    }

    renderPreCrossword() {
        if (this.store.state === STATES.LOADING) {
            return (<div>
                <p>Generating a surprise crossword for you...</p>
            </div>)
        }
        if (this.store.state === STATES.FETCHING) {
            return (<div>
                <p>Fetching the crossword now</p>
            </div>)
        }
        return (<div>
                <span>Generate a entirely new crossword for you:</span>
                <button onClick={() => this.createNewCrossword()}>Create new crossword</button>
            </div>
        )
    }

    renderWaitForCrosswordLoad() {
        return (<div>
            <p>Loading an entirely unique new crossword for you ...</p>
            <FidgetSpinner height={"80"} with={"80"} radius={"9"} ariaLabel="loading"/>
        </div>)
    }

    render() {
        return (
            <div className="container">
                <h1>Crossword</h1>
                {!this.store.isLoaded && !this.store.crosswordId && this.renderPreCrossword()}
                {!this.store.isLoaded && this.store.crosswordId && this.renderWaitForCrosswordLoad()}
                {this.store.isLoaded && <BoardReactComponent crossword={this.store.crossword} />}
            </div>
        )
    }
}