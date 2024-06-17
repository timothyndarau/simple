import React, { useEffect, useState } from 'react';
import { fetchData } from '../ApiService';

const Dashboard = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        const getData = async () => {
            const result = await fetchData();
            setData(result);
        };
        getData();
    }, []);

    return (
        <div>
            <h1>Environmental Data Dashboard</h1>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Temperature</th>
                        <th>Humidity</th>
                        <th>Air Quality</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((entry) => (
                        <tr key={entry.id}>
                            <td>{entry.id}</td>
                            <td>{entry.temperature}</td>
                            <td>{entry.humidity}</td>
                            <td>{entry.air_quality}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Dashboard;
