import React from "react";
import * as api from "../helpers/api.js"
import StreetList from "./StreetList"

class StreetIndex extends React.Component {


    constructor(props) {
        super(props);
        let match = props.match;
        let page = parseInt(match.params.page);
        this.state = {
            showStreets: false,
            city: match.params.city,
            page: page,
            streets: null,
            cities: ["Edinburgh"],
            //TODO make the range of pages dynamic
            next_pages: this.range(1, 41, 1),
        };
    }

    range = (start, stop, step) => Array.from({length: (stop - start) / step + 1}, (_, i) => start + (i * step));

    componentDidMount() {
        api.getStreetsPaged(this.state.city, this.state.page).then(resp => {
            if (resp.length > 0) {
                this.setState({
                    showStreets: true,
                    streets: resp,
                });
            }
        })
    }


    render() {
        return (
            <div className="p-2 container-fluid text-center">
                {this.state.showStreets ?
                    <div className="row justify-content-center">
                        <StreetList streets={this.state.streets}/>
                        {this.state.next_pages.map(page =>
                            <a key={page} className="p-2" href={"/StreetIndex/" + this.state.city + "/" + page}>{page}</a>)}
                    </div>


                    :
                    ""
                }
            </div>
        )
    }
}

export default StreetIndex;