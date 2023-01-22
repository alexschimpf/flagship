import * as React from 'react';
import {
    BrowserRouter, Routes, Route
} from 'react-router-dom';
import Header from '../header';
import Footer from '../footer';
import Main from '../pages/main';
import Login from '../pages/login';
import SetPassword from '../pages/setPassword';
import NotFound from '../pages/notFound';

function App(): React.ReactElement {
    return (
        <BrowserRouter>
            <div>
                <div>
                    <Header />
                    <Routes>
                        <Route path='/' element={<Main />} />
                        <Route path='/login' element={<Login />} />
                        <Route path='/set-password' element={<SetPassword />} />
                        <Route path='*' element={<NotFound />} />
                    </Routes>
                </div>
                <Footer />
            </div>
        </BrowserRouter>
    );
}

export default App;
