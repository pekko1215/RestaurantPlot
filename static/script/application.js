const $name = document.getElementById('name');
const $comment = document.getElementById('comment')
const $latitude = document.getElementById('latitude');
const $longitude = document.getElementById('longitude');
const $moveCenter = document.getElementById('moveCenter');
const $postPlot = document.getElementById('postPlot');

mapboxgl.accessToken = 'pk.eyJ1IjoicGVra28xMjE1IiwiYSI6ImNrOGZtd2h5YzA1ejAzcnBmaWFlMWdrZWcifQ.oJY75kM9DXxj17fS1_JSlw';
const Map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v9',
    center: [139.76670289945957, 35.68951119845987],
    zoom: 9.5
});

const Plots = [];
let DraggableMarker = null;

const Main = async() => {
    let p = await fetch('/api/plot', {
        method: 'GET'
    })
    let data = await p.json();
    data.forEach(p => {
        let popUp = document.createElement('div');
        popUp.classList.add('plot')

        let title = document.createElement('div');
        title.classList.add('plot-name')
        title.innerText = p.name;

        let comment = document.createElement('div')
        comment.classList.add('plot-comment')
        comment.innerText = p.comment

        let name = document.createElement('div');
        name.classList.add('plot-createby')
        name.innerText = p.createdBy


        popUp.appendChild(title)
        popUp.appendChild(comment)
        popUp.appendChild(name)

        popUp.addEventListener('click', () => {
            Map.setCenter([p.x, p.y])
        })

        document.getElementById('plotList').appendChild(popUp)
        let marker = new mapboxgl.Marker({ color: 'green' })
            .setLngLat([p.x, p.y])
            .setPopup(new mapboxgl.Popup({ offset: 25 })
                .setHTML(popUp.innerHTML))
            .addTo(Map)
        Plots.push(p)
        if(p.isMine){
            let deleteButton = document.createElement('button');
            deleteButton.classList.add('plot-delete');
            deleteButton.innerText = '削除'
            popUp.appendChild(deleteButton)
            deleteButton.addEventListener('click',async()=>{
                if(!confirm(`${p.name}を削除しますか？`)){
                    return    
                }
                let f = await fetch('/api/plot/'+p.id,{method:'DELETE'})
                if(await f.text() === 'ok'){
                    alert('削除しました')
                    location.reload()
                }else{
                    alert('削除に失敗しました')                    
                }
            })
        }
    })

    const refreshMarker = () => {
        let lngLat = DraggableMarker.getLngLat();
        $latitude.value = lngLat.lat;
        $longitude.value = lngLat.lng;
    }
    DraggableMarker = new mapboxgl.Marker({
            draggable: true,
            color: 'orange'
        })
        .setLngLat(Map.getCenter())
        .addTo(Map)
        .on('dragend', refreshMarker)
    $moveCenter.addEventListener('click', () => {
        DraggableMarker.setLngLat(Map.getCenter())
    })

    refreshMarker();

    $postPlot.addEventListener('click', async() => {
        $postPlot.disabled = true;
        let form = new FormData();
        form.append('x', $longitude.value)
        form.append('y', $latitude.value)
        form.append('comment', $comment.value)
        form.append('name', $name.value)

        let data = await fetch('/api/plot', {
            method: 'POST',
            body: form
        });
        if (await data.text() === 'ok') {
            alert('投稿されました')
            location.reload()
        } else {
            alert('投稿に失敗しました。入力を確かめてください。')
        }

    })
}

Main();
