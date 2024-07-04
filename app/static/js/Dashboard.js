import React, { useEffect, useState } from 'react';

const Dashboard = () => {
    const [userInfo, setUserInfo] = useState(null);

    useEffect(() => {
        const fetchUserInfo = async () => {
            const response = await fetch('/api/dashboard', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                },
            });
            const data = await response.json();
            setUserInfo(data);
        };

        fetchUserInfo();
    }, []);

    if (!userInfo) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>Welcome, {userInfo.name}</h1>
            <h2>Your Activities</h2>
            <ul>
                {userInfo.activities.map((activity, index) => (
                    <li key={index}>{activity}</li>
                ))}
            </ul>
            <h2>Your Events</h2>
            <ul>
                {userInfo.events.map((event, index) => (
                    <li key={index}>{event}</li>
                ))}
            </ul>
        </div>
    );
};

export default Dashboard;
