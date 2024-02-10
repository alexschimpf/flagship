export default function Footer() {
    const currYear = new Date().getFullYear();

    return (
        <footer className='sticky z-50 w-full border-t bottom-0'>
            <div className='container flex h-10 max-w-screen-2xl items-center justify-center'>
                <div>
                    <h1>&copy; {currYear}</h1>
                </div>
            </div>
        </footer>
    );
}
