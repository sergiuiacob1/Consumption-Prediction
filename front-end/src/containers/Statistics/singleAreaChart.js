import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import { randomColor } from 'randomcolor'

export class SingleAreaChart extends React.Component {

    render() {
        return (
            <div>
                <h1>{this.props.titleKey}</h1>
                <AreaChart width={600} height={400} data={this.props.data}
                    margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey={this.props.xAxisKey} />
                    <YAxis />
                    <Tooltip />
                    <Area type='monotone' dataKey="data" stroke={randomColor()} fill={randomColor()} />
                </AreaChart>
            </div>
        );
    }
}