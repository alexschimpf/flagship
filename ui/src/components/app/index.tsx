import * as React from 'react';
import {
    BrowserRouter, Routes, Route
} from 'react-router-dom';
import './index.css';
import Header from '../header';
import Main from '../pages/main';
import Login from '../pages/login';
import ForgotPassword from '../pages/forgotPassword';
import SetPassword from '../pages/setPassword';
import NotFound from '../pages/notFound';

function App(): React.ReactElement {
    return (
        <BrowserRouter>
            <div className='app'>
                <div className='app--header'>
                    <Header />
                </div>
                <div className='app--main'>
                    <Routes>
                        <Route path='/' element={<Main />} />
                        <Route path='/login' element={<Login />} />
                        <Route path='/forgot-password' element={<ForgotPassword />} />
                        <Route path='/set-password' element={<SetPassword />} />
                        <Route path='*' element={<NotFound />} />
                    </Routes>
                </div>
            </div>
        </BrowserRouter>
    );
}

export default App;
