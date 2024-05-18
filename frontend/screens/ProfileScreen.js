import React, { useEffect, useState } from 'react';
import { View, Text } from 'react-native';
import axios from 'axios';

const ProfileScreen = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:5000/api/users/someUserId')
      .then(response => setUser(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <View>
      {user ? <Text>{user.name}</Text> : <Text>Loading...</Text>}
    </View>
  );
};

export default ProfileScreen;
