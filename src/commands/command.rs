use std::convert::TryFrom;
use std::io;

use super::dispatch::Dispatch;
use super::list::List;

#[derive(Debug)]
pub struct TryFromStringForCommand(());

#[derive(Debug)]
pub enum Command<'a> {
    List(List<'a>),
    Dummy,
}

impl<'a> Command<'a> {
    pub fn as_list(&self) -> Option<&List<'a>> {
        match self {
            Command::List(list) => Some(list),
            _ => None,
        }
    }
}

impl<'a> TryFrom<&'a [&'a str]> for Command<'a> {
    type Error = TryFromStringForCommand;
    fn try_from(value: &'a [&'a str]) -> Result<Command<'a>, Self::Error> {
        if value.is_empty() {
            return Err(TryFromStringForCommand(()));
        }
        if value.len() >= 2 && value[0] == "list" {
            let lst = List::from(value[1]);
            Ok(Command::List(lst))
        } else {
            println!("nope 2");
            Err(TryFromStringForCommand(()))
        }
    }
}

impl<'a> Dispatch for Command<'a> {
    type Error = io::Error;
    fn dispatch(&self) -> Result<(), Self::Error> {
        match self {
            Command::List(list) => list.dispatch(),
            _ => unimplemented!(),
        }
    }
}

#[test]
#[should_panic]
fn test_unable_to_create_command_with_invalid_commands() {
    Command::try_from(&[][..]).unwrap();
    Command::try_from(&["invalid_command"][..]).unwrap();
}

#[test]
fn test_create_list_command() {
    let command = Command::try_from(&["list", "/user"][..]).expect("should create command");
    assert_eq!(
        command.as_list().expect("should be list"),
        &List::from("/user")
    );
}
