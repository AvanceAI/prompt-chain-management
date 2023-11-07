// SideBar.js
import { Drawer, List, ListItem, ListItemText } from "@material-ui/core";

const mockMessages = [
  { message: 'Hello World', variable: { opt1: 'data', opt2: 'data2', opt3: 'data3' } },
  { message: 'Test Message 2', variable: { another1: 'piece', another2: 'piece2', another3: 'piece3' } },
  // Add as many mock messages as you like
];

export default function SideBar({ onSendMockMessage }) {
    return (
        <>
            <Drawer variant="permanent" anchor="left">
                <div style={{ width: '150px' }}>
                    <List>
                        {mockMessages.map((mock, index) => (
                            <ListItem 
                                button 
                                key={mock.message}
                                onClick={() => onSendMockMessage(mock)}
                            >
                                <ListItemText primary={`Mock ${index + 1}`} />
                            </ListItem>
                        ))}
                    </List>
                </div>
            </Drawer>
        </>
    );
}
