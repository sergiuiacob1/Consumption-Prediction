import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { randomColor } from 'randomcolor'

export class SingleBarChart extends React.Component {


    buildGraphBar(keys) {
        var bars = []
        for (const key in keys) {
            bars.push(<Bar dataKey={keys[key]} fill={randomColor()} />)
        }
        return bars;
    }

    render() {
        return (
            <div>
                <h1>{this.props.titleKey}</h1>
                <BarChart width={1000} height={300} data={this.props.data}
                    margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey={this.props.xAxisKey} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    {this.buildGraphBar(this.props.statKey)}
                </BarChart>
            </div>
        );
    }
}