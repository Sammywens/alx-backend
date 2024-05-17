import { createClient } from 'redis';

const client = createClient();

client.on('error', err => {
  console.error('Redis client error:', err);
});

const updateHash = (hashName, fieldValues) => {
  client.hmset(hashName, fieldValues, (err, reply) => {
    if (err) {
      console.error('Error updating hash:', err);
    } else {
      console.log('Hash updated successfully:', reply);
    }
  });
};

const printHash = async (hashName) => {
  try {
    const hashData = await new Promise((resolve, reject) => {
      client.hgetall(hashName, (err, reply) => {
        if (err) {
          reject(err);
        } else {
          resolve(reply);
        }
      });
    });
    console.log('Hash data:', hashData);
  } catch (error) {
    console.error('Error getting hash:', error);
  }
};

async function main() {
  const hashObj = {
    Portland: 50,
    Seattle: 80,
    'New York': 20,
    Bogota: 20,
    Cali: 40,
    Paris: 2,
  };

  const fields = [];
  for (const [field, value] of Object.entries(hashObj)) {
    fields.push(field, value.toString());
  }

  updateHash('HolbertonSchools', fields);
  await printHash('HolbertonSchools');
}

client.on('connect', () => {
  console.log('Redis client connected to the server');
  main().catch(error => {
    console.error('Main function error:', error);
  });
});
