pub trait Dispatch {
    type Error;
    fn dispatch(&self) -> Result<(), Self::Error>;
}
