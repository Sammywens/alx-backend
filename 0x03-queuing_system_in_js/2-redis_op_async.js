import { promisify } from 'util';
import { createClient } from 'redis';

const client = createClient();

client.on('error', err => {
  console.error('Redis client error:', err);
});

const setNewSchool = (schoolName, value) => {
  client.set(schoolName, value, (err, reply) => {
    if (err) {
      console.error('Error setting value:', err);
    } else {
      console.log('Value set successfully:', reply);
    }
  });
};

const displaySchoolValue = async schoolName => {
  try {
    const getAsync = promisify(client.get).bind(client);
    const value = await getAsync(schoolName);
    console.log(`Value for ${schoolName}:`, value);
  } catch (error) {
    console.error('Error getting value:', error);
  }
};

async function main() {
  console.log('Starting main...');
  await displaySchoolValue('Holberton');
  setNewSchool('HolbertonSanFrancisco', '100');
  await displaySchoolValue('HolbertonSanFrancisco');
  console.log('Main finished.');
}

client.on('connect', async () => {
  console.log('Redis client connected to the server');
  await main();
});
