import React from 'react';

import './App.css'
import Routes from './Components/Routes';
import { BrowserRouter } from 'react-router-dom';
import { SnackbarProvider } from 'notistack';
function App() {
  return (
    <>
      <SnackbarProvider anchorOrigin={{
      vertical: 'bottom',
      horizontal: 'center',
    }}>
      <BrowserRouter>
        <Routes />
      </BrowserRouter>
      </SnackbarProvider>
    </>
  );
}

export default App;