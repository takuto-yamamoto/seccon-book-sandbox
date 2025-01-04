import express, { Request, Response } from 'express';

const app = express();
const PORT = 8888;

const users = [
  { name: 'Alice', password: 'a' },
  { name: 'Bob', password: 'b' },
  { name: 'Charlie', password: 'c' },
];

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.get('/', (_req: Request, res: Response) => {
  res.send(`<!DOCTYPE html>
    <html>
      <head></head>
      <body>
        <form action="/api" method="POST">
          Name: <input type="text" name="name">
          Password: <input type="text" name="password">
          <input type="submit" value="Submit">
        </form>
      </body>
    </html>`);
});

app.post('/api', (req: Request, res: Response): Response => {
  const { name, password } = req.body;

  const user = users.find((user) => user.name === name);
  if (!user) {
    return res.status(401).send('Incorrect.');
  }
  if (user.password === password) {
    return res.status(200).send(`Logged in as ${user.name}.`);
  } else {
    return res.status(401).send('Incorrect.');
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
