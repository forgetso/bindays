import React from "react";


class StreetList extends React.Component {


    constructor(props) {
        super(props);
        this.gethref = this.gethref.bind(this);
    }


    gethref = function (city, street) {
        return "/" + city.toLowerCase() + "/" + street.replaceAll(" ", "_").toLowerCase()
    };


    render() {
        return (
            <div className="p-2 container-fluid text-center">
                <div className="row justify-content-center">
                    <ul className="list-unstyled">{this.props.streets.map((item) => (
                        <li key={item['_id']} className="text-center">
                            <a href={this.gethref(item['city'], item['_id'])}>{item['_id']}, {item['city']}</a>
                        </li>
                    ))}</ul>
                </div>

            </div>
        )
    }
}

export default StreetList;