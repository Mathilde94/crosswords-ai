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

    render() {
        if (!this.store.isLoaded && !this.store.crosswordId) {
            if (this.store.state === STATES.LOADING) {
                return (<div>
                    <h2>Feeling Lucky</h2>
                    <p>Generating a surprise crossword for you...</p>
                </div>)
            }
            if (this.store.state === STATES.FETCHING) {
                return (<div>
                    <h2>Feeling Lucky</h2>
                    <p>Fetching the crossword now</p>
                </div>)
            }
            return (<div>
                <h2>Feeling Lucky?</h2>
                <span>Generate a entirely new crossword for you:</span>
                <button onClick={() => this.createNewCrossword()}>Create new crossword</button>
            </div>)
        }
        if (!this.store.isLoaded || this.store.crossword === null) {
            return (<div>
                <h2>Feeling Lucky</h2>
                <p>Loading an entirely unique new crossword for you ...</p>
                <FidgetSpinner height={"80"} with={"80"} radius={"9"} ariaLabel="loading"/>
            </div>)
        }
        return (
            <div className="container">
                <h1>Crossword</h1>
                <BoardReactComponent crossword={this.store.crossword} />
            </div>
        )
    }
}