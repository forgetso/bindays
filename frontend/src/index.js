import 'bootstrap/dist/css/bootstrap.css';
import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import Street from './components/Street'
import StreetIndex from './components/StreetIndex'
import reportWebVitals from './reportWebVitals';
import {Route, BrowserRouter as Router, Link} from 'react-router-dom'

ReactDOM.render(
    <React.StrictMode>
        <Router>
            <div className="row">
                <div className="text-center mx-auto">
                    <img className="" src="favicon.ico"/>
                    <h1 className="m-t-10">
                        <a href="/">Bin Days</a>
                    </h1>
                </div>
            </div>
            <Route exact path="/" component={App}/>
            <Route exact path="/StreetIndex/:city/:page" component={StreetIndex}/>
            <Route exact path="/:city/:street" component={Street}/>
            <nav className="navbar navbar-light">
                <Link className="navbar-nav mx-auto" to="/"> Home </Link>{" "}
                <Link className="navbar-nav mx-auto" to="/StreetIndex/Edinburgh/1">Index </Link>{" "}
            </nav>
        </Router>

    </React.StrictMode>,
    document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
