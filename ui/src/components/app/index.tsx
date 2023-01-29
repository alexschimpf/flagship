import * as React from 'react';
import {
    BrowserRouter, Routes, Route
} from 'react-router-dom';
import './index.css';
import Header from '../header';
import Main from '../main';
import Login from '../login';
import ForgotPassword from '../forgotPassword';
import SetPassword from '../setPassword';
import NotFound from '../notFound';

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
                        <Route path='/users' element={<Main />} />
                        <Route path='/profile' element={<Main />} />
                        <Route path='*' element={<NotFound />} />
                    </Routes>
                </div>
            </div>
        </BrowserRouter>
    );
}

export default App;
