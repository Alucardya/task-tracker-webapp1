import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { TaskProvider } from './TaskContext';

const theme = createTheme({
  palette: {
    mode: 'light',
  },
});

ReactDOM.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <TaskProvider>
        <App />
      </TaskProvider>
    </ThemeProvider>
  </React.StrictMode>,
  document.getElementById('root')
);
