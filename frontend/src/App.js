import React, {Component} from 'react';
import './App.css';
import * as api from "./helpers/api.js"
import StreetList from "./components/StreetList"


function App() {
    return (
        <div className="App p-2">
            <BinDays></BinDays>
        </div>
    );
}

class BinDays extends Component {
    constructor(props) {
        super(props);
        this.state = {
            showInput: false,
        };
        this.reload = this.reload.bind(this);
    }

    componentDidMount() {
        this.setState({
            showInput: true,
        });
    }

    reload() {
        this.componentDidMount();
    }

    render() {
        return (
            <div className="container-fluid">
                <SearchBox id="search"/>
            </div>

        );
    }

}

class SearchBox extends React.Component {

    constructor(props) {
        super(props);
        this.props = props;
        this.state = {'streets': [], lastSearchTime: 0, searchTerm: ""};
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange = (event) => {
        const searchTerm = event.target.value;
        const theTime = Date.now();
        let timeDiff = theTime - this.state.lastSearchTime;

        const searchTermStripped = searchTerm.replace(searchTerm.match(/^[0-9]+\s*/), "");

        if (searchTermStripped.length > 4 && timeDiff > 300) {
            this.setState({lastSearchTime: Date.now()});

            api.searchSteets(searchTerm).then((resp) => {
                let sortedResp = resp.sort((a, b) => (a._id > b._id) ? 1 : -1);
                console.log(sortedResp);
                this.setState({
                    streets: sortedResp,
                    searchTerm: searchTerm
                });


            }).catch(err => console.log('There was an error:' + err));
        }

    };


    render() {
        return (
            <div className="form-group">
                <label htmlFor="street">Search for your street</label>
                <input type="text" id="street"
                       onChange={this.handleChange}
                       className="form-control"/>
                {this.state.streets.length > 0 ?
                    <div className="p-2">
                        <StreetList streets={this.state.streets}/>
                    </div>
                    : ""
                }
            </div>
        )
    }

}


export default App;
