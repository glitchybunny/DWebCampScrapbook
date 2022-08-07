var file_list=[], name_list=[], desc_list=[];

// Script to format bytes to kb/mb/whatever for uploads, source: https://stackoverflow.com/questions/15900485/correct-way-to-convert-size-in-bytes-to-kb-mb-gb-in-javascript
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// The file upload code was modified from my own https://github.com/darkrilin/rat-graphing/
// Run all this once the page is ready
window.addEventListener('load', function(){

    // Check when file changes
    var ALLOWED_EXTENSIONS = ['.jpe','.jpg','.jpeg','.gif','.png','.bmp','.ico','.svg','.svgz','.tif','.tiff','.ai','.drw','.pct','.psp','.xcf','.psd','.raw'];

    function allowed_file(filename){
        return filename.includes(".") && ALLOWED_EXTENSIONS.includes("." + filename.split(".").slice(-1));
    }

    document.getElementById('file-input').addEventListener('change', function(){
        if (this.value){
            var table, row;
            table = document.getElementById('file-table');

            // flush all elements from table
            while (table.children.length > 1) {
                table.removeChild(table.lastChild);
            }

            // add new elements to table (sorry if this is super ugly)
            file_list = [];
            name_list = [];
            desc_list = [];
            let n = document.getElementById("file-input").files.length;
            for (let i=0, f; f = document.getElementById("file-input").files[i]; i++) {
                row = document.createElement('tr');

                let cell_file = document.createElement('td');
                cell_file.append(document.createTextNode(f.name));
                cell_file.style.maxWidth = '130px';
                cell_file.style.wordWrap = 'break-word';

                let cell_name = document.createElement('td');
                let cell_name_input = document.createElement('input');
                cell_name_input.classList.add('name-input');
                cell_name_input.tabIndex = 1;
                if ((i === 0) && (n > 1)) {
                    let cell_name_all = document.createElement('a');
                    cell_name_all.classList.add('name-all-button');
                    cell_name_all.append(document.createTextNode('⬇️'));
                    cell_name_all.href = "#";
                    cell_name_all.onclick = function() {
                        let super_name = name_list[0].value;
                        if (super_name !== "") {
                            for (let j=1; j<name_list.length; j++) {name_list[j].value = super_name;}
                        }
                    };
                    cell_name.append(cell_name_input, cell_name_all);
                } else {
                    cell_name.append(cell_name_input);
                }

                let cell_desc = document.createElement('td');
                let cell_desc_input = document.createElement('textarea');
                cell_desc_input.classList.add('desc-input');
                cell_desc_input.tabIndex = 2;
                cell_desc.append(cell_desc_input);

                let cell_size = document.createElement('td');
                cell_size.append(document.createTextNode(formatBytes(f.size)));

                row.append(cell_file, cell_name, cell_desc, cell_size);
                table.append(row);

                file_list.push(f);
                name_list.push(cell_name_input);
                desc_list.push(cell_desc_input);
            }
            document.getElementById("file-table").style.display = "table";
            document.getElementById("no-files-chosen").style.display = "none";

            // enable upload button
            document.getElementById('submit-btn').disabled = false;
        } else {
            document.getElementById("file-table").style.display = "none";
            document.getElementById("no-files-chosen").style.display = "block";

            // disable upload button
            document.getElementById('submit-btn').disabled = true;
        }
    });

    // Open file dialog when import is pressed
    document.getElementById("import-btn").addEventListener('click', function(){
        document.getElementById('file-input').click();
    });

    // Submit - read file and generate the chart from that data.
    document.getElementById('submit-btn').addEventListener("click", function(){
        if (file_list.length !== 0) {
            if (allowed_file(file_list[0].name)) {
                let target = document.getElementById('target');

                for (let i=0; i<file_list.length; i++) {
                    var h_name = document.createElement('input');
                    h_name.name = 'name_' + i;
                    h_name.style.display = 'none';
                    h_name.value = name_list[i].value;

                    var h_desc = document.createElement('input');
                    h_desc.name = 'desc_' + i;
                    h_desc.style.display = 'none';
                    h_desc.value = desc_list[i].value;

                    target.append(h_name, h_desc);
                }

                target.submit();
            }
            else{
                alert("Please only upload images for the moment");
            }
        }
        else{
            alert("Please select a file");
        }
    });
});
