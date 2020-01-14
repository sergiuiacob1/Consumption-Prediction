import React from 'react';

export default class Statistics extends React.Component {
    constructor() {
        super();
        this.state = {
            statisticsData: {}
        };
    }

    componentDidMount() {
        fetch('http://localhost:3001/general_statistics', {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            }
        })
            .then(response => {
                this.setState({ statisticsData: response.json() })
            })
    }

    renderTableForKey(key) {
        const { statisticsData } = this.state

        if (statisticsData[key] === undefined) {
            return;
        }

        console.log("ACOLO");

        return (<div>CEVA NORMAL</div>)
    }

    render() {
        return (
            <div className="container" >
                <div className="row mb-3" >
                    <div className="col" >
                        {this.renderTableForKey("biomass")}
                    </div>
                </div>
            </div >
        );

    }
}