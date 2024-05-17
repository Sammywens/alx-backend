import { createQueue } from 'kue';

const BLACKLISTED_NUMBERS = new Set(['4153518780', '4153518781']);// Use a Set for faster lookups
const queue = createQueue();

/**
 * Sends a push notification to a user.
 * @param {String} phoneNumber
 * @param {String} message
 * @param {Job} job
 * @param {*} done
 */
const sendNotification = (phoneNumber, message, job, done) => {
  let total = 2;
  let sendInterval = setInterval(() => {
    if (total - job._retries <= total / 2) { // Use _retries property for retries count
      job.progress(total - job._retries, total);
    }
    if (BLACKLISTED_NUMBERS.has(phoneNumber)) { // Use has() method for Set
      done(new Error(`Phone number ${phoneNumber} is blacklisted`));
      clearInterval(sendInterval);
      return;
    }
    if (job._retries === total) {
      console.log(
        `Sending notification to ${phoneNumber},`,
        `with message: ${message}`,
      );
    }
    job._retries--;
    if (job._retries === 0) {
      clearInterval(sendInterval);
      done();
    }
  }, 1000);
};

queue.process('push_notification_code_2', 2, (job, done) => {
  // Extract job data to improve readability
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});

