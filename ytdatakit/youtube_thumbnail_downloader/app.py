import streamlit as st
from ytdatakit.youtube_thumbnail_downloader.state import state_init
from ytdatakit.youtube_thumbnail_downloader.callbacks import fetch_thumbnails
import tempfile


def app():
    state_init()
    with tempfile.TemporaryDirectory() as savedir:
        st.markdown(
            """
        <style>
        .element-container:has(style){
            display: none;
        }
        #button-download {
            display: none;
        }
        .element-container:has(#button-download) {
            display: none;
        }
        .element-container:has(#button-download) + div button {
            background-color: green;
            border-color: green;
            }
        #button-fetch {
            display: none;
        }
        .element-container:has(#button-fetch) {
            display: none;
        }
        .element-container:has(#button-fetch) + div button {
            background-color: blue;
            border-color: blue;
            }
        </style>
        """,
            unsafe_allow_html=True,
        )

        base = st.container(border=True)
        with base:
            text_urls = st.text_area(
                "youtube urls separated by commas",
                value=st.session_state.thumbnail_raw_urls,
                placeholder="https://www.youtube.com/shorts/o7a9hx-Pqyo, https://www.youtube.com/shorts/xkAYLnIsfX4, ....",
                key="thumbnail_urls_input"
            )
            uploaded_file = st.file_uploader("Choose a File", type=["txt"], key="thumbanils_file_uploader")
            thumbnail_col_1, thumbnail_col_2, thumbnail_col_3 = st.columns([5, 4, 6])
            with thumbnail_col_1:
                st.markdown('<span id="button-fetch"></span>', unsafe_allow_html=True)
                fetch_btn = st.button(
                    label="fetch thumbnails",
                    type="primary",
                )
                if fetch_btn:
                    fetch_thumbnails(uploaded_file, text_urls, savedir)

            # with thumbnail_col_2:
            #     st.markdown('<span id="button-download"></span>', unsafe_allow_html=True)
            #     st.download_button(
            #         label="download thumbnails",
            #         data=st.session_state.thumbnails_zip_path,
            #         file_name="thumbnails.zip",
            #         mime="application/zip",
            #         disabled=False,
            #         type="primary",
            #         on_click=fetch_thumbnails,
            #         args=(uploaded_file, text_urls)
            #     )
            
            with st.container(border=True):            
                for ind, thumbnail_savepath in enumerate(st.session_state.thumbnail_savepaths):
                    title = st.session_state.thumbnail_data_entries[ind]["video_title"]
                    thumbnail_savepath = st.session_state.thumbnail_savepaths[ind]
                    with st.container(border=True):
                        a, b, c = st.columns([1, 3, 1])
                        with b:
                            st.subheader(title)
                            st.image(thumbnail_savepath)
                            with open(thumbnail_savepath, "rb") as file:
                                st.download_button(
                                    label="download thumbnail",
                                    data=file,
                                    file_name=title,
                                    mime="image/jpg",
                                    key=f"{title} download",
                                    type="primary",
                                )