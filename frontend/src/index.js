import './style.css';
import { createRoot } from 'react-dom/client';
import CrosswordReactComponent from './crossword/crossword.react-component';

function reactMountElement() {
    const element = document.createElement('main');
    element.id = 'root';
    return element;
}

function App() {
    return (
        <div>
            <CrosswordReactComponent />
        </div>
    );}

document.body.appendChild(reactMountElement());
const root = createRoot(document.getElementById('root'));
root.render(<App />);