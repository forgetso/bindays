import React from "react";
import * as api from "../helpers/api.js"

class Street extends React.Component {


    constructor(props) {
        super(props);
        let match = props.match;
        this.state = {
            showInput: false,
            days: {},
            street: match.params.street,
            city: match.params.city,

        };
    }

    componentDidMount() {
        api.getStreet(this.state.city, this.state.street).then(resp => {
            if (resp.length > 0) {
                this.setState({
                    showInput: true,
                    days: resp
                });
                console.log(resp);
            }
        })
    }

    capitalizeName = function (name) {
        return name.replace(/\b(\w)/g, s => s.toUpperCase());
    };


    render() {
        return (
            <div className="p-2 container-fluid text-center">
                <div>
                    <div className="row  justify-content-center">
                        <h2 className="mb-3">{this.capitalizeName(this.state.street.replaceAll("_", " "))}</h2>
                    </div>
                </div>
                {this.state.showInput ?
                    <div>
                        <div className="row  justify-content-center">
                            <div className="p-10">
                                <span className="mb-3">Next bin
                                    day: {new Date(this.state.days[0]['date']).toLocaleDateString('en', {
                                        day: '2-digit',
                                        weekday: 'long',
                                        month: 'long',
                                    })}</span>
                            </div>
                        </div>
                        <div className="row  justify-content-center">
                            <ul className="binList">
                                {this.state.days[0]['bins'].map(bin => <li className="bin" key={bin}>
                                    <figure>
                                        <img className="img-responsive inline-block"
                                             alt={bin + " bin"}
                                             src={"/images/" + bin + ".png"}/>
                                        <figcaption>{this.capitalizeName(bin) + " bin"}</figcaption>
                                    </figure>
                                </li>)}
                            </ul>
                        </div>
                        <div className="row  justify-content-center">
                            <div>
                                <h4>Future bin days</h4>
                                <ul className="list-unstyled">
                                    {this.state.days.map((item, i) => <li
                                        key={i}>{new Date(item['date']).toLocaleDateString('en', {
                                        day: '2-digit',
                                        weekday: 'long',
                                        month: 'long',
                                        year: 'numeric'
                                    })}</li>)}
                                </ul>
                            </div>
                        </div>
                    </div>
                    :
                    ""
                }
            </div>
        )
    }
}

export default Street;