const hierachy = {
    id: 'ms',
    data: {
        imageURL: 'https://i.pravatar.cc/300?img=68',
        name: 'PLACE',
    },
    options: {
        nodeBGColor: '#cdb4db',
        nodeBGColorHover: '#cdb4db',
    },
    children: [
        {
            id: 'mh',
            data: {
                imageURL: 'https://i.pravatar.cc/300?img=69',
                name: 'FEATURE',
            },
            options: {
                nodeBGColor: '#ffafcc',
                nodeBGColorHover: '#ffafcc',
            },
            children: [
                {
                    id: 'kb',
                    data: {
                        imageURL: 'https://i.pravatar.cc/300?img=65',
                        name: 'ARTIFACT 1',
                    },
                    options: {
                        nodeBGColor: '#f8ad9d',
                        nodeBGColorHover: '#f8ad9d',
                    },
                },
                {
                    id: 'cr',
                    data: {
                        imageURL: 'https://i.pravatar.cc/300?img=60',
                        name: 'ARTIFACT 2',
                    },
                    options: {
                        nodeBGColor: '#c9cba3',
                        nodeBGColorHover: '#c9cba3',
                    },
                },
            ],
        },
    ],
};

const options = {
    contentKey: 'data',
    nodeWidth: 150,
    nodeHeight: 100,
    fontColor: '#fff',
    borderColor: '#333',
    childrenSpacing: 50,
    siblingSpacing: 20,
    direction: 'top',
    enableExpandCollapse: true,
    nodeTemplate: (content) =>
        `<div style='display: flex; flex-direction: column; gap: 10px; justify-content: center; align-items: center; height: 100%;'>
          <img style='width: 50px; height: 50px; border-radius: 50%;' src='${content.imageURL}' alt='' />
          <div style="font-weight: bold; font-family: Arial; font-size: 14px">${content.name}</div>
         </div>`,
    canvasStyle: 'background: #f6f6f6;',
    enableToolbar: true,
};

const tree = new ApexTree(document.getElementById('svg-tree'), options);
tree.render(hierachy);
